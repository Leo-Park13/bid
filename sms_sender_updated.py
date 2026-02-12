import os
import re
import json
import time
import hmac
import hashlib
import base64
from datetime import datetime
from tkinter import Tk, filedialog, messagebox

import pandas as pd
import requests
import chardet
from dotenv import load_dotenv

# ----------------------------------------
# 0) .env 로드 (Windows / macOS 공용)
# ----------------------------------------
load_dotenv()
NCP_ACCESS_KEY = os.getenv("NCP_ACCESS_KEY")
NCP_SECRET_KEY = os.getenv("NCP_SECRET_KEY")
NCP_SERVICE_ID = os.getenv("NCP_SERVICE_ID")
NCP_SENDER     = os.getenv("NCP_SENDER")


def require_env():
    missing = [k for k, v in {
        "NCP_ACCESS_KEY": NCP_ACCESS_KEY,
        "NCP_SECRET_KEY": NCP_SECRET_KEY,
        "NCP_SERVICE_ID": NCP_SERVICE_ID,
        "NCP_SENDER": NCP_SENDER,
    }.items() if not v]

    if missing:
        print("❌ .env 파일 설정이 부족합니다.")
        print("누락된 항목: {}".format(", ".join(missing)))
        print("\n예시 .env 내용:")
        print("NCP_ACCESS_KEY=발급받은AccessKey")
        print("NCP_SECRET_KEY=발급받은SecretKey")
        print("NCP_SERVICE_ID=ncp:sms:kr:123456789012:sens-service")
        print("NCP_SENDER=01012345678")
        raise SystemExit(1)


# ----------------------------------------
# 1) 안전한 문자열 변환 (NaN / None 방어)
# ----------------------------------------
def safe_text(v):
    """NaN / None / float 등 어떤 값이 와도 안전하게 str로 변환"""
    if v is None:
        return ""
    if isinstance(v, float) and pd.isna(v):
        return ""
    return str(v).strip()


def safe_float(v):
    """안전한 float 변환 (견인거리 계산용)"""
    if v is None or pd.isna(v):
        return 0.0
    try:
        # 문자열에서 숫자만 추출 (예: "12.5km" → 12.5)
        s = str(v).strip()
        s = re.sub(r'[^\d.]', '', s)
        return float(s) if s else 0.0
    except:
        return 0.0


# ----------------------------------------
# 2) 파일 선택 (윈도우 / 맥 GUI 공용)
# ----------------------------------------
def select_file(title="CSV 파일 선택"):
    root = Tk()
    root.withdraw()
    path = filedialog.askopenfilename(
        title=title,
        filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
    )
    root.destroy()
    return path


# ----------------------------------------
# 3) 이모지(4바이트 유니코드) 제거 — SENS가 거절하는 문자
# ----------------------------------------
_emoji_re = re.compile(r"[\U00010000-\U0010FFFF]+")


def remove_emoji(s):
    if not isinstance(s, str):
        return s
    return _emoji_re.sub("", s)


# ----------------------------------------
# 4) CSV 인코딩 자동감지 + 구분자 자동추론 + 숫자열 보존
#    - Excel UTF-16 / CP949 / UTF-8-SIG 전부 대응
# ----------------------------------------
def read_csv_auto(path):
    with open(path, "rb") as f:
        raw = f.read(120_000)
    detected = chardet.detect(raw)
    enc = detected.get("encoding") or "utf-8"
    print("🔍 감지된 인코딩: {}".format(enc))

    encodings = [enc, "utf-8-sig", "cp949", "utf-16", "utf-16le", "utf-16be"]

    # 1차: sep=None으로 자동 추론 시도
    for en in encodings:
        try:
            df = pd.read_csv(path, encoding=en, engine="python", sep=None, dtype=str)
            print("✅ {} 인코딩 + 자동 구분자 로드 성공 ({}행)".format(en, len(df)))
            return df
        except Exception as e:
            print("⚠️ {} 인코딩 자동구분자 실패: {}".format(en, e))

        # 2차: 흔한 구분자 수동 시도
        for sep in [",", "\t", ";", "|"]:
            try:
                df = pd.read_csv(path, encoding=en, engine="python", sep=sep, dtype=str)
                print("✅ {} + sep='{}' 로드 성공 ({}행)".format(en, sep, len(df)))
                return df
            except Exception:
                pass

    raise ValueError("❌ CSV 파일을 읽을 수 없습니다. 인코딩/구분자를 확인해주세요.")


# ----------------------------------------
# 5) contact.csv 자동 생성
# ----------------------------------------
def auto_generate_contact_csv(call_df, output_path="contact.csv"):
    """
    고장출동리스트.csv에서 운수사 목록을 추출하여 contact.csv 생성
    사용자가 담당자번호와 담당자번호2를 입력할 수 있는 템플릿 생성
    """
    call_company_col = "운수사"
    
    if call_company_col not in call_df.columns:
        raise ValueError("❌ 긴급출동리스트.csv에 '{}'컬럼이 없습니다.".format(call_company_col))
    
    # 운수사 고유 목록 추출 (NaN 제외)
    companies = call_df[call_company_col].dropna().unique()
    companies = [safe_text(c) for c in companies if safe_text(c) and safe_text(c) != "미기재"]
    
    # contact.csv 생성
    contact_template = pd.DataFrame({
        "운수사명": companies,
        "담당자번호": [""] * len(companies),
        "담당자번호2": [""] * len(companies)
    })
    
    contact_template.to_csv(output_path, index=False, encoding="utf-8-sig")
    print("\n✅ {} 파일이 생성되었습니다!".format(output_path))
    print("📝 총 {}개 운수사가 등록되었습니다.".format(len(companies)))
    print("💡 {} 파일을 열어서 담당자번호를 입력해주세요.\n".format(output_path))
    
    return output_path


# ----------------------------------------
# 6) Naver Cloud SENS 문자 발송
# ----------------------------------------
def send_sms(to, content):
    # 전화번호는 숫자만
    to = re.sub(r"\D", "", str(to))
    # 이모지 제거
    content = remove_emoji(content)

    url = "https://sens.apigw.ntruss.com/sms/v2/services/{}/messages".format(NCP_SERVICE_ID)
    timestamp = str(int(time.time() * 1000))
    message = "POST /sms/v2/services/{}/messages\n{}\n{}".format(
        NCP_SERVICE_ID, timestamp, NCP_ACCESS_KEY
    )

    signature = base64.b64encode(
        hmac.new(
            NCP_SECRET_KEY.encode("utf-8"),
            message.encode("utf-8"),
            hashlib.sha256
        ).digest()
    ).decode("utf-8")

    headers = {
        "x-ncp-apigw-timestamp": timestamp,
        "x-ncp-iam-access-key": NCP_ACCESS_KEY,
        "x-ncp-apigw-signature-v2": signature,
        "Content-Type": "application/json; charset=utf-8",
    }

    body = {
        "type": "LMS",
        "contentType": "COMM",
        "countryCode": "82",
        "from": NCP_SENDER,
        "content": content,
        "messages": [{"to": to}],
    }

    try:
        resp = requests.post(
            url,
            headers=headers,
            data=json.dumps(body, ensure_ascii=False).encode("utf-8"),
            timeout=15
        )
        if resp.status_code == 202:
            print("✅ 전송 성공 → {}".format(to))
        else:
            print("❌ 전송 실패 ({}): {}".format(to, resp.text))
    except Exception as e:
        print("⚠️ 전송 중 오류 ({}): {}".format(to, e))


# ----------------------------------------
# 7) 메인 로직
# ----------------------------------------
def main():
    require_env()
    print("=" * 60)
    print("📱 SMS 자동 발송 프로그램 v2.0")
    print("=" * 60)
    print("\n📂 고장출동리스트.csv 파일을 선택해주세요.\n")

    # 1단계: 고장출동리스트.csv 선택
    call_path = select_file("긴급출동리스트.csv 선택")
    if not call_path:
        print("❌ 파일 선택이 취소되어 프로그램을 종료합니다.")
        return

    # 2단계: 긴급출동리스트 로드
    call_df = read_csv_auto(call_path)
    call_df.columns = [c.strip() for c in call_df.columns]
    
    print("\n📊 긴급출동리스트 로드 완료: {}건".format(len(call_df)))
    print("🔍 컬럼 목록: {}\n".format(list(call_df.columns)))
    
    # 3단계: contact.csv 자동 생성 여부 확인
    contact_path = "contact.csv"
    
    if os.path.exists(contact_path):
        print("ℹ️ 기존 {} 파일이 존재합니다.".format(contact_path))
        use_existing = input("기존 파일을 사용하시겠습니까? (Y/N): ").strip().lower()
        
        if use_existing != "y":
            print("\n🔄 새로운 {} 파일을 생성합니다...".format(contact_path))
            auto_generate_contact_csv(call_df, contact_path)
            print("\n📝 {} 파일에 담당자 전화번호를 입력한 후 Enter를 눌러주세요.".format(contact_path))
            input("계속하려면 Enter를 누르세요...")
    else:
        print("\n🔄 {} 파일이 없습니다. 자동으로 생성합니다...".format(contact_path))
        auto_generate_contact_csv(call_df, contact_path)
        print("\n📝 {} 파일에 담당자 전화번호를 입력한 후 Enter를 눌러주세요.".format(contact_path))
        input("계속하려면 Enter를 누르세요...")
    
    # 4단계: contact.csv 로드
    if not os.path.exists(contact_path):
        print("❌ {} 파일이 없습니다.".format(contact_path))
        return
    
    contact_df = read_csv_auto(contact_path)
    contact_df.columns = [c.strip() for c in contact_df.columns]
    
    print("\n✅ 담당자 목록 로드 완료: {}개 운수사".format(len(contact_df)))

    # 필요한 컬럼명 정의
    contact_name_col   = "운수사명"
    contact_phone_col  = "담당자번호"
    contact_phone_col2 = "담당자번호2"
    call_company_col   = "운수사"
    call_km_col        = "견인거리"  # 견인거리 컬럼
    call_detail_col    = "조치상세"  # ← 요청 내용 대신 조치상세 사용

    # 컬럼 존재 확인
    for col in [contact_name_col, contact_phone_col]:
        if col not in contact_df.columns:
            raise ValueError("❌ contact.csv에 '{}' 컬럼이 없습니다. 현재 컬럼: {}".format(
                col, list(contact_df.columns)
            ))
    
    if call_company_col not in call_df.columns:
        raise ValueError("❌ 긴급출동리스트.csv에 '{}' 컬럼이 없습니다. 현재 컬럼: {}".format(
            call_company_col, list(call_df.columns)
        ))
    
    # 조치상세 컬럼 확인 (없으면 경고만 표시)
    if call_detail_col not in call_df.columns:
        print("⚠️ 경고: '{}' 컬럼이 없습니다. 기본값으로 처리됩니다.".format(call_detail_col))
        call_df[call_detail_col] = ""
    
    # 견인거리 컬럼 확인 (없으면 0으로 처리)
    if call_km_col not in call_df.columns:
        print("⚠️ 경고: '{}' 컬럼이 없습니다. 견인거리는 0으로 표시됩니다.".format(call_km_col))
        call_df[call_km_col] = 0

    # 운수사별 담당자 전화번호 매핑 (담당자번호 + 담당자번호2)
    contacts_by_company = {}
    for _, row in contact_df.iterrows():
        comp   = safe_text(row.get(contact_name_col))
        phone1 = re.sub(r"\D", "", safe_text(row.get(contact_phone_col)))
        phone2 = re.sub(r"\D", "", safe_text(row.get(contact_phone_col2, "")))
        
        if comp:
            phone_set = set()
            if phone1 and len(phone1) >= 10:
                phone_set.add(phone1)
            if phone2 and len(phone2) >= 10:
                phone_set.add(phone2)
            
            if phone_set:
                contacts_by_company[comp] = phone_set

    # 운수사별 그룹 (NaN → "미기재")
    grouped = call_df.groupby(call_df[call_company_col].fillna("미기재"))
    print("\n📦 {}개 운수사 데이터 수집 완료\n".format(len(grouped)))

    # 미리보기
    print("=" * 60)
    print("📋 발송 예정 내용 미리보기")
    print("=" * 60)
    
    preview_count = 0
    for company, grp in grouped:
        company = safe_text(company)
        if company == "미기재":
            continue
        
        to_list = list(contacts_by_company.get(company, []))
        if not to_list:
            continue
        
        # 견인거리 합계 계산
        total_km = sum(safe_float(row.get(call_km_col, 0)) for _, row in grp.iterrows())
        
        print("\n📌 운수사: {}".format(company))
        print("   담당자: {}".format(', '.join(to_list)))
        print("   출동건수: {}건".format(len(grp)))
        print("   총 견인거리: {:.1f}km".format(total_km))
        
        preview_count += 1
        if preview_count >= 3:
            print("\n... (이하 생략)")
            break
    
    print("\n" + "=" * 60)
    yn = input("🟢 실제 문자 전송을 진행하시겠습니까? (Y/N): ").strip().lower()
    if yn != "y":
        print("🛑 전송이 취소되었습니다.")
        return

    # 운수사별 문자 생성 및 발송
    total_sent = 0
    for company, grp in grouped:
        company = safe_text(company)

        if company == "미기재":
            print("ℹ️ 운수사 미기재 {}건 → 건너뜀".format(len(grp)))
            continue

        to_list = list(contacts_by_company.get(company, []))
        if not to_list:
            print("ℹ️ {} 담당자번호 없음 → 건너뜀".format(company))
            continue

        # 견인거리 합계 계산
        total_km = sum(safe_float(row.get(call_km_col, 0)) for _, row in grp.iterrows())

        # 문자 본문 구성
        lines = [
            "안녕하세요 스마트라이드 입니다.",
            "{} 긴급출동 요약보고".format(datetime.now().strftime('%Y.%m.%d')),
            "운수사: {}".format(company),
            "총 {}건".format(len(grp)),
            "견인 거리: {:.1f}KM".format(total_km),
            "",
        ]

        # 상위 5건만 요약 표시 (조치상세 사용)
        for i, (_, r) in enumerate(grp.head(5).iterrows(), 1):
            car    = safe_text(r.get("차량번호", ""))
            detail = safe_text(r.get(call_detail_col, ""))
            
            # 조치상세가 비어있으면 기본 메시지
            if not detail:
                detail = "조치 완료"
            
            lines.append("{}. {} / {}".format(i, car, detail))

        lines.append("")
        lines.append("세부내역은 월말에 취합 후 전달 예정입니다.")
        lines.append("감사합니다.")
        message = "\n".join(lines)

        # 실제 전송
        print("\n📤 {} 발송 중...".format(company))
        for phone in to_list:
            send_sms(phone, message)
            total_sent += 1
            time.sleep(0.5)  # API 과부하 방지

    print("\n" + "=" * 60)
    print("✅ 모든 문자 전송 완료! (총 {}건 발송)".format(total_sent))
    print("=" * 60)


# ----------------------------------------
# 8) 진입점
# ----------------------------------------
if __name__ == "__main__":
    main()
