# GUI 버전

import tkinter as tk
from tkinter import messagebox
import random
from collections import Counter



def format_number(event):           # 기초 금액
    value = entry_base.get().replace(",", "")
    if value.isdigit():
        entry_base.delete(0, tk.END)
        entry_base.insert(0, "{:,}".format(int(value)))


# 공 금액 생성 함수
def generate_ball_dict(base, percent, order):       
    min_value = base - (base * percent / 100)       # -n 적용
    max_value = base + (base * percent / 100)       # +n 적용

    values = [0] * 15   # 최대금액 최소금액 기초금액 설정 및 가격을 15개의 공 배치
    values[0] = int(min_value)
    values[7] = int(base)
    values[14] = int(max_value)

    lower_step = (base - min_value) / 7     # 기초금액 보단 작은 수 -n%
    for i in range(1, 7):
        values[i] = int(min_value + lower_step * i)

    upper_step = (max_value - base) / 7     # 기초금액 보단 큰 수 +n%
    for i in range(8, 14):
        values[i] = int(base + upper_step * (i - 7))

    if order == 'desc':     # 정렬 방식을 내림차순으로 선택시 공 배치를 거꾸로 돌린다
        values.reverse()

    return {i + 1: values[i] for i in range(15)}    # 공에 금액을 배치 할때 i 하나에 금액 하나 i는 +1씩 증가한다


def calculate():                        # 계산 함수
    try:
        base = int(entry_base.get().replace(",", ""))
        bid_rate = float(entry_bid.get()) / 100     # 투찰율 % 적용
        company_count = int(entry_company.get())    # 예상 참여 업체수 (랜덤 공 출력 횟수)
        percent = 2 if percent_var.get() == 1 else 3    # +- 퍼센트 적용
        order = 'asc' if order_var.get() == 1 else 'desc'   # 정렬 방식 적용

        selected_balls = [i + 1 for i, var in enumerate(ball_vars) if var.get() == 1]       # 1번부터 15번 까지 공 선택택
        if not selected_balls or not all(1 <= n <= 15 for n in selected_balls):
            raise ValueError("1~15 사이의 공 번호를 최소 1개 이상 선택해주세요.")

        ball_dict = generate_ball_dict(base, percent, order)        # 공 리스트에 금액 배치

        history = []        # 공 선택 후 다시 랜덤의 공 출력
        history.extend(selected_balls)
        for _ in range(company_count):          # 예상업체수 만큼 랜덤 횟수 
            picks = random.sample(range(1, 16), 2)      # 15개의 공에서 2개를 선택
            history.extend(picks)                   # 리스트에 추가가
        

        counter = Counter(history)      # history 리스트의 랜덤 횟수를 카운트
        top_four = [num for num, _ in counter.most_common(4)]   # 가장 많이 출력된 4개의 공 출력
        top_values = [ball_dict[i] for i in top_four]       # 랜덤 출력된 공들이 탑4 리스트에 들어감 

        final_balls = top_four               # 전체 공에서 탑4 출력
        final_values = top_values              # 선택된 공 리스트를 다시 리스트화 하기
        total = sum(final_values)               # 최종금액의 합
        avg = total / len(final_values)         # 최종금액의 평균
        result_bid = int(avg * bid_rate)        # 평균 금액에 투찰율 적용

        # 전체 결과 텍스트 출력
        full_text = "[공 배치]\n"
        for i in range(1, 16):
            full_text += "{}번 공 → {:,} 원\n".format(i, ball_dict[i])

        full_text += "\n[선택된 공 번호 및 금액]\n"
        for i in selected_balls:
            full_text += "- {}번 공: {:,} 원\n".format(i, ball_dict[i])

        full_text += "\n[자동 추첨 공 번호 및 횟수]\n"
        for i in top_four:
            full_text += "- {}번 공: {} 회\n".format(i, counter[i])

        full_text += "\n사용된 공 번호:\n"
        for i in final_balls:
            full_text += "- {}번 공: {:,} 원\n".format(i, ball_dict[i])
        full_text += "\n[투찰율 적용 금액 ({}%)]: {:,} 원\n".format(bid_rate * 100, result_bid)

        full_text += "\n[계산 결과]\n"
        full_text += "총합: {:,} 원\n".format(total)
        full_text += "평균 금액 (총 {}개 공): {:,} 원\n".format(len(final_values), int(avg))

        result_output_full.delete("1.0", tk.END)
        result_output_full.insert(tk.END, full_text)

        result_output_final.config(bg="#333", fg="white")
        result_output_final.delete("1.0", tk.END)
        result_output_final.insert(tk.END, "\t{:,}".format(result_bid))

    except Exception as e:
        messagebox.showerror("오류", "입력 오류: {}".format(e))



# === GUI 구성 ===
root = tk.Tk()
root.title("투찰 계산기")

main_frame = tk.Frame(root)
main_frame.pack(padx=10, pady=10)

frame_inputs = tk.Frame(main_frame)
frame_inputs.grid(row=0, column=0, sticky="n")

# 전체 결과 출력창
result_output_full = tk.Text(main_frame, height=30, width=60, font=("Helvetica", 11))
result_output_full.grid(row=0, column=1, padx=(20, 0))

tk.Label(main_frame, text="계산 결과  -> 최종금액", font=("Helvetica", 12, "bold")).grid(row=1, column=1, sticky="w", pady=(10, 0))

final_result_frame = tk.Frame(main_frame)
final_result_frame.grid(row=2, column=1, sticky="w", pady=(5, 0))

result_output_final = tk.Text(final_result_frame, height=1, width=18, font=("Helvetica", 12, "bold"))
result_output_final.pack(side="left")
tk.Label(final_result_frame, text="원", font=("Helvetica", 12, "bold")).pack(side="right", padx=(5, 0))

# 입력 필드 구성
tk.Label(frame_inputs, text="기초 금액 (원)", font=("Helvetica", 11)).grid(row=0, column=0, sticky="w")
entry_base = tk.Entry(frame_inputs, font=("Helvetica", 11), width=20)
entry_base.grid(row=0, column=1)
entry_base.bind("<KeyRelease>", format_number)

tk.Label(frame_inputs, text="투찰율 (%)", font=("Helvetica", 11)).grid(row=1, column=0, sticky="w")
entry_bid = tk.Entry(frame_inputs, font=("Helvetica", 11), width=20)
entry_bid.grid(row=1, column=1)

tk.Label(frame_inputs, text="예상 업체 수", font=("Helvetica", 11)).grid(row=2, column=0, sticky="w")
entry_company = tk.Entry(frame_inputs, font=("Helvetica", 11), width=20)
entry_company.grid(row=2, column=1)

# 공 번호 체크박스
tk.Label(frame_inputs, text="공 번호 선택 (1~15)", font=("Helvetica", 11, "bold")).grid(row=3, column=0, sticky="w", pady=(10, 0))
ball_vars = [tk.IntVar() for _ in range(15)]
checkbox_frame = tk.Frame(frame_inputs)
checkbox_frame.grid(row=4, column=0, columnspan=3, sticky="w")

for i in range(15):
    tk.Checkbutton(checkbox_frame, text="{}번".format(i + 1), variable=ball_vars[i], font=("Helvetica", 10)).grid(row=i // 5, column=i % 5, sticky="w")

# 퍼센트 선택
percent_var = tk.IntVar(value=1)
tk.Label(frame_inputs, text="± 퍼센트 선택", font=("Helvetica", 11)).grid(row=5, column=0, sticky="w", pady=(10, 0))
tk.Radiobutton(frame_inputs, text="±2%", variable=percent_var, value=1, font=("Helvetica", 11)).grid(row=5, column=1, sticky="w")
tk.Radiobutton(frame_inputs, text="±3%", variable=percent_var, value=2, font=("Helvetica", 11)).grid(row=5, column=2, sticky="w")

# 정렬 방식 선택
order_var = tk.IntVar(value=1)
tk.Label(frame_inputs, text="정렬 방식", font=("Helvetica", 11)).grid(row=6, column=0, sticky="w")
tk.Radiobutton(frame_inputs, text="오름차순", variable=order_var, value=1, font=("Helvetica", 11)).grid(row=6, column=1, sticky="w")
tk.Radiobutton(frame_inputs, text="내림차순", variable=order_var, value=2, font=("Helvetica", 11)).grid(row=6, column=2, sticky="w")

# 계산 버튼
btn_calculate = tk.Button(frame_inputs, text="계산하기", command=calculate, font=("Helvetica", 14, "bold"), bg="#4CAF50", fg="white", width=15, height=2)
btn_calculate.grid(row=7, column=0, columnspan=3, pady=15)

root.mainloop()





# python 버전(수정중)

import random
from collections import Counter


def get_random_values(num, percent_input, Bnum, order):
    # min, max 계산
    percent = (num * (percent_input / 100))
    min_value = num - percent
    max_value = num + percent

    # 15등분 리스트 만들기
    diff = max_value - min_value
    step = diff / 15
    value_list = [min_value + step * i for i in range(16)]

    # 정렬 옵션
    if order == "2":  # 내림차순
        value_list.reverse()

    # 공 번호와 값 매핑 (1번~15번)
    ball_dict = {i: int(value_list[i]) for i in range(1, 16)}

    # N개 랜덤 추출
    random_indexes = random.sample(range(1, 16), Bnum)
    random_values = [(i, ball_dict[i]) for i in random_indexes]

    # 출력
    print("\n===== 공 배치 =====")
    for i in range(1, 16):
        print("{}번 공 → {:,} 원".format(i, ball_dict[i]))

    print("\n===== 랜덤 추출된 공 =====")
    for i, val in random_values:
        print("{}번 공 → {:,} 원".format(i, val))

    print("\n{}의 ±{}% 범위는 {:,} 원 ~ {:,} 원 입니다."
          .format(int(num), percent_input, int(min_value), int(max_value)))

    return random_values, ball_dict


# 실행
Snum = int(input("기준 금액을 입력하세요: "))
Bnum = int(input("몇 개의 공 번호를 선택하시겠습니까? : "))

Bresult = []

while len(Bresult) < Bnum:
    num = int(input("{}번째로 선택할 공 번호 (1~15): ".format(len(Bresult) + 1)))

    if num in Bresult:
        print("이미 선택한 번호입니다. 다시 입력하세요.\n")
        continue
    if not (1 <= num <= 15):
        print("1번부터 15번 사이 숫자만 입력 가능합니다.\n")
        continue

    Bresult.append(num)

print("\n!!!번호 선택 완료!!!")
print("\n내가 선택한 공 → {}".format(", ".join("{}번".format(n) for n in Bresult)))

percent_input = int(input("+-의 값을 입력하세요: "))
choice = int(input("투찰율 유형을 선택하세요 (1: 88.7%, 2: 87.745%): "))
if choice == 1:
    bidnum = 0.887
elif choice == 2:
    bidnum = 0.87745
else:
    print("1번 또는 2번 중 골라 주세요")
    exit()

order_choice = input("공 배치 금액 정렬 방식을 선택하세요 (1: 오름차순, 2: 내림차순): ")

CompanyCount = int(input("예상 업체수는 얼마 일까요?: "))

result, ball_dict = get_random_values(Snum, percent_input, Bnum, order_choice)

# 업체수 입력 받아 그 수만큼 자동 추첨 시작 하는데 입력 받은 숫자 2개도 포함 랜덤 돌리기
random_history = []

for _ in range(CompanyCount):
    random_indexes = random.sample(range(1, 16), 2)
    random_history.extend(random_indexes)
random_indexes.append(Bresult)

counter = Counter(random_history)


# 자동으로 가장 많이 선택된 번호 4개
top_four = counter.most_common(4)

# 최종 선택된 4개 공 번호
final_selected = [num for num, _ in top_four]

# 최종 4개 공 금액 계산
final_values = [ball_dict[n] for n in final_selected]
final_sum = sum(final_values)
final_avg = final_sum / len(final_values)

# 평균을 입력 받은 투찰율로 계산
deduct = final_avg * bidnum

# ===== 결과 출력 =====
print("\n===== 결과 =====")
print("\n내가 선택한 공 → {}".format(", ".join("{}번".format(n) for n in Bresult)))

print("\n자동으로 가장 많이 선택된 번호:")
for num, count in top_four:
    print("{}번 ({}회)".format(num, count))

print("\n!!! 최종 선택된 4개 공 !!!")
for n in final_selected:
    price = ball_dict.get(n)
    print(" → {}번 ({:,} 원)".format(n, price))

print("\n최종 선택된 4개 공의 금액 합계: {:,} 원".format(final_sum))
print("최종 선택된 4개 공의 금액 평균: {:,} 원".format(int(final_avg)))
print("평균 금액의 투찰율({:.3f}%) 계산 결과: {:,} 원".format(bidnum * 100, int(deduct)))
