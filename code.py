1차 

import random
from collections import Counter

  
def get_random_values(num, percent_input, Bnum):
    # min, max 계산
    percent = (num * (percent_input / 100))
    min_value = num - percent
    max_value = num + percent

    # 15등분 리스트 만들기
    diff = max_value - min_value
    step = diff / 15
    value_list = [min_value + step * i for i in range(16)]

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

CompanyCount = int(input("예상 업체수는 얼마 일까요?: "))

result, ball_dict = get_random_values(Snum, percent_input, Bnum)

# 업체수 입력 받아 그 수만큼 자동 추첨 시작
random_history = []

for _ in range(CompanyCount):
    random_indexes = random.sample(range(1, 16), 2)
    random_history.extend(random_indexes)

counter = Counter(random_history)

# 평균 계산
values = [val for _, val in result]
average = sum(values) / len(values)
deduct = average * bidnum

# 자동으로 가장 많이 선택된 번호 2개
top_two = counter.most_common(2)

# ===== 결과 출력 =====
print("\n===== 결과 =====")
print("\n선택하신 공 (공 번호): {}"
      .format(", ".join("{}번".format(n) for n in Bresult)))

print("추출된 {}개의 번호와 금액".format(Bnum))
for i, val in result:
    print("{}번 공 → {:,} 원".format(i, val))

print("\n내가 선택한 공 → {}번, {}번".format(Bresult[0], Bresult[1]))
print("내가 선택한 공의 금액 합계: {:,} 원".format(sum(values)))

print("\n자동으로 가장 많이 선택된 번호:")
for num, count in top_two:
    print("{}번 ({}회)".format(num, count))

# 최종 선택된 4개 공 번호
final_selected = Bresult[:2] + [num for num, _ in top_two]

print("\n★★★ 최종 선택된 4개 공 ★★★")
for n in final_selected:
    price = ball_dict.get(n)
    print(f" → {n}번 ({price:,} 원)")

# 최종 4개 공 금액 계산
final_values = [ball_dict[n] for n in final_selected]
final_sum = sum(final_values)
final_avg = final_sum / len(final_values)

print("\n최종 선택된 4개 공의 금액 합계: {:,} 원".format(final_sum))
print("최종 선택된 4개 공의 금액 평균: {:,} 원".format(int(final_avg)))

print("\n추출된 공 금액 평균: {:,} 원".format(int(average)))
print("평균 금액의 투찰율 계산 결과: {:,} 원".format(int(deduct)))


2차 + 선택한 2개의 공과 랜덤 선택 2개의 공의 평균 수정 및 선택한 투찰율 출력

import random
from collections import Counter


def get_random_values(num, percent_input, Bnum):
    # min, max 계산
    percent = (num * (percent_input / 100))
    min_value = num - percent
    max_value = num + percent

    # 15등분 리스트 만들기
    diff = max_value - min_value
    step = diff / 15
    value_list = [min_value + step * i for i in range(16)]

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

CompanyCount = int(input("예상 업체수는 얼마 일까요?: "))

result, ball_dict = get_random_values(Snum, percent_input, Bnum)

# 업체수 입력 받아 그 수만큼 자동 추첨 시작
random_history = []

for _ in range(CompanyCount):
    random_indexes = random.sample(range(1, 16), 2)
    random_history.extend(random_indexes)

counter = Counter(random_history)

# 자동으로 가장 많이 선택된 번호 2개
top_two = counter.most_common(2)

# 최종 선택된 4개 공 번호
final_selected = Bresult[:2] + [num for num, _ in top_two]

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
for num, count in top_two:
    print("{}번 ({}회)".format(num, count))

print("\n!!! 최종 선택된 4개 공 !!!")
for n in final_selected:
    price = ball_dict.get(n)
    print(f" → {n}번 ({price:,} 원)")

print("\n최종 선택된 4개 공의 금액 합계: {:,} 원".format(final_sum))
print("최종 선택된 4개 공의 금액 평균: {:,} 원".format(int(final_avg)))
print("평균 금액의 투찰율({:.3f}%) 계산 결과: {:,} 원"
      .format(bidnum * 100, int(deduct)))


3차 + 공 금액 배치 오름차순 내림차순 선택

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

# 업체수 입력 받아 그 수만큼 자동 추첨 시작
random_history = []

for _ in range(CompanyCount):
    random_indexes = random.sample(range(1, 16), 2)
    random_history.extend(random_indexes)

counter = Counter(random_history)

# 자동으로 가장 많이 선택된 번호 2개
top_two = counter.most_common(2)

# 최종 선택된 4개 공 번호
final_selected = Bresult[:2] + [num for num, _ in top_two]

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
for num, count in top_two:
    print("{}번 ({}회)".format(num, count))

print("\n!!! 최종 선택된 4개 공 !!!")
for n in final_selected:
    price = ball_dict.get(n)
    print(" → {}번 ({:,} 원)".format(n, price))

print("\n최종 선택된 4개 공의 금액 합계: {:,} 원".format(final_sum))
print("최종 선택된 4개 공의 금액 평균: {:,} 원".format(int(final_avg)))
print("평균 금액의 투찰율({:.1f}%) 계산 결과: {:,} 원".format(bidnum * 100, int(deduct)))


# 코드 수정본 1차

import random
from collections import Counter

# 공 배치 및 랜덤 번호 추출 함수
def get_random_values(num, percent_input, Bnum, order):
    # ±2% 계산
    percent = (num * (percent_input / 100))
    min_value = num - percent
    max_value = num + percent

    # 15등분 리스트 만들기
    diff = max_value - min_value
    step = diff / 15
    value_list = [min_value + step * i for i in range(16)]

    # 1번과 15번은 고정
    value_list[1] = min_value  # 1번 공은 최저값
    value_list[15] = max_value  # 15번 공은 최고값
    value_list[8] = num  # 8번 공은 기준 금액 고정

    # 정렬 옵션
    if order == "2":  # 내림차순
        value_list.reverse()

    # 공 번호와 값 매핑 (1번~15번)
    ball_dict = {i: int(value_list[i]) for i in range(1, 16)}

    # # N개 랜덤 추출
    # random_indexes = random.sample(range(1, 16), Bnum)
    # random_values = [(i, ball_dict[i]) for i in random_indexes]

    # 출력
    print("\n===== 공 배치 =====")
    for i in range(1, 16):
        print("{}번 공 → {:,} 원".format(i, ball_dict[i]))

    # print("\n===== 랜덤 추출된 공 =====")
    # for i, val in random_values:
    #     print("{}번 공 → {:,} 원".format(i, val))

    print("\n{}의 ±{}% 범위는 {:,} 원 ~ {:,} 원 입니다."
          .format(int(num), percent_input, int(min_value), int(max_value)))

    return ball_dict

# ======================
# 사용자 입력 처리
# ======================
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

# 공 배치 및 랜덤 번호 추출
ball_dict = get_random_values(Snum, percent_input, Bnum, order_choice)

# ======================
# 선택된 공 2개 + 랜덤 2개 포함해서 업체 수만큼 랜덤 돌리기
# ======================

random_history = []

for _ in range(CompanyCount):
    # Bresult 2개 번호 포함
    selected = list(Bresult)

    # 선택된 Bresult 포함 나머지 1~15 중에서 랜덤 4개 추출
    remaining_numbers = list(set(range(1, 16)))
    extra_randoms = random.sample(remaining_numbers, 4)

    selected.extend(extra_randoms)
    random_history.extend(selected)

# 가장 많이 등장한 번호 4개 추출
counter = Counter(random_history)
top_four = counter.most_common(4)

# 최종 선택된 번호와 금액 계산
final_selected = [num for num, _ in top_four]
final_values = [ball_dict[n] for n in final_selected]
final_sum = sum(final_values)
final_avg = final_sum / len(final_values)
deduct = final_avg * bidnum

# ======================
# 출력 결과
# ======================
print("\n===== 선택한 공 2개 -> 랜덤 4개 최종 결과 =====")
print("가장 많이 선택된 번호 (혼합 기준):")
for Rnum, count in top_four:
    print(" → {}번 ({}회)".format(Rnum, count))

print("\n최종 선택된 4개 공 (혼합 기준):")
for n in final_selected:
    price = ball_dict.get(n)
    print(" → {}번 ({:,} 원)".format(n, price))

print("\n합계: {:,} 원".format(final_sum))
print("평균: {:,} 원".format(int(final_avg)))
print("투찰율 적용({:.3f}%): {:,} 원".format(bidnum * 100, int(deduct)))


4차 GUI 사용

import tkinter as tk
from tkinter import messagebox
import random
from collections import Counter

def generate_ball_dict(base, percent, order):
    min_value = base - (base * percent / 100)
    max_value = base + (base * percent / 100)
    step = (max_value - min_value) / 15
    values = [int(min_value + step * i) for i in range(16)]
    if order == 'desc':
        values.reverse()
    return {i: values[i] for i in range(1, 16)}

def calculate():
    try:
        base = int(entry_base.get())
        bid_rate = float(entry_bid.get()) / 100
        company_count = int(entry_company.get())
        percent = 2 if percent_var.get() == 1 else 3
        order = 'asc' if order_var.get() == 1 else 'desc'

        user_input = entry_balls.get()
        selected_balls = [int(x.strip()) for x in user_input.split(',') if x.strip().isdigit()]

        if not selected_balls or not all(1 <= n <= 15 for n in selected_balls):
            raise ValueError("1~15 사이의 공 번호를 쉼표로 입력해주세요 .")

        ball_dict = generate_ball_dict(base, percent, order)
        selected_values = [ball_dict[i] for i in selected_balls]

        history = []
        for _ in range(company_count):
            picks = random.sample(range(1, 16), 2)
            history.extend(picks)

        counter = Counter(history)
        top_two = [num for num, _ in counter.most_common(2)]
        top_values = [ball_dict[i] for i in top_two]

        final_balls = selected_balls + top_two
        final_values = selected_values + top_values
        total = sum(final_values)
        avg = total / len(final_values)
        result_bid = int(avg * bid_rate)

        result_text = ""
        result_text +="[공 배치]\n"
        for i in range(1,16):
            result_text += "- {}번 공: {:,} 원\n".format(i, ball_dict[i])
        result_text += "\n[선택된 공 번호 및 금액]\n"
        for i in selected_balls:
            result_text += "- {}번 공: {:,} 원\n".format(i, ball_dict[i])

        result_text += "\n[자동 추첨 공 번호 및 금액]\n"
        for i in top_two:
            result_text += "- {}번 공: {:,} 원\n".format(i, ball_dict[i])

        result_text += "\n[계산 결과]\n"
        result_text += "사용된 공 번호: {}\n".format(", ".join(str(n) for n in final_balls))
        result_text += "총합: {:,} 원\n".format(total)
        result_text += "{}개의 공의 평균 금액: {:,} 원\n".format(len(final_values), int(avg))
        result_text += "투찰율 적용 금액 ({}%): {:,} 원\n".format(bid_rate * 100, result_bid)

        result_output.delete("1.0", tk.END)
        result_output.insert(tk.END, result_text)

    except Exception as e:
        messagebox.showerror("오류", "입력 오류: {}".format(e))


root = tk.Tk()
root.title("투찰 계산기")

frame_inputs = tk.Frame(root)
frame_inputs.pack(padx=25, pady=25)

tk.Label(frame_inputs, text="기초 금액 (원)").grid(row=0, column=0, sticky="w")
entry_base = tk.Entry(frame_inputs)
entry_base.grid(row=0, column=2)

tk.Label(frame_inputs, text="투찰율 (%)").grid(row=1, column=0, sticky="w")
entry_bid = tk.Entry(frame_inputs)
entry_bid.grid(row=1, column=2)

tk.Label(frame_inputs, text="선택할 공 번호 ").grid(row=2, column=0, sticky="w")
entry_balls = tk.Entry(frame_inputs)
entry_balls.grid(row=2, column=2, columnspan=2)

tk.Label(frame_inputs, text="예상 업체 수").grid(row=3, column=0, sticky="w")
entry_company = tk.Entry(frame_inputs)
entry_company.grid(row=3, column=2)

percent_var = tk.IntVar(value=1)
tk.Label(frame_inputs, text="± 퍼센트 선택").grid(row=4, column=0, sticky="w")
tk.Radiobutton(frame_inputs, text="±2%", variable=percent_var, value=1).grid(row=4, column=1, sticky="w")
tk.Radiobutton(frame_inputs, text="±3%", variable=percent_var, value=2).grid(row=4, column=2, sticky="w")

order_var = tk.IntVar(value=1)
tk.Label(frame_inputs, text="정렬 방식").grid(row=5, column=0, sticky="w")
tk.Radiobutton(frame_inputs, text="오름차순", variable=order_var, value=1).grid(row=5, column=1, sticky="w")
tk.Radiobutton(frame_inputs, text="내림차순", variable=order_var, value=2).grid(row=5, column=2, sticky="w")


btn_calculate = tk.Button(root, text="계산하기", command=calculate)
btn_calculate.pack(pady=5)

result_output = tk.Text(root, height=15, width=60)
result_output.pack(padx=15, pady=15)

root.mainloop()




# + GUI에 추가 할것 -> 금액 입력 칸에 (,콤마) 들어가게 하기, 계산하기 버튼 키우기, []안의 글씨 굵은 글씨로 변경하기
# 금액 칸 따로 만들기 8번 공은 기초금액 고정 1번공은 -n% 15번공은 +n% 고정 하기

# 4 아마 최종


import tkinter as tk
from tkinter import messagebox
import random
from collections import Counter


def format_number(event):
    value = entry_base.get().replace(",", "")
    if value.isdigit():
        entry_base.delete(0, tk.END)
        entry_base.insert(0, "{:,}".format(int(value)))


# 공 금액 생성 함수
def generate_ball_dict(base, percent, order):
    min_value = base - (base * percent / 100)
    max_value = base + (base * percent / 100)

    values = [0] * 15
    values[0] = int(min_value)
    values[7] = int(base)
    values[14] = int(max_value)

    lower_step = (base - min_value) / 7
    for i in range(1, 7):
        values[i] = int(min_value + lower_step * i)

    upper_step = (max_value - base) / 7
    for i in range(8, 14):
        values[i] = int(base + upper_step * (i - 7))

    if order == 'desc':
        values.reverse()

    return {i + 1: values[i] for i in range(15)}


def calculate():
    try:
        base = int(entry_base.get().replace(",", ""))
        bid_rate = float(entry_bid.get()) / 100
        company_count = int(entry_company.get())
        percent = 2 if percent_var.get() == 1 else 3
        order = 'asc' if order_var.get() == 1 else 'desc'

        selected_balls = [i + 1 for i, var in enumerate(ball_vars) if var.get() == 1]
        if not selected_balls or not all(1 <= n <= 15 for n in selected_balls):
            raise ValueError("1~15 사이의 공 번호를 최소 1개 이상 선택해주세요.")

        ball_dict = generate_ball_dict(base, percent, order)
        selected_values = [ball_dict[i] for i in selected_balls]

        history = []
        history.extend(selected_balls)
        for _ in range(company_count):
            picks = random.sample(range(1, 16), 2)
            history.extend(picks)
        

        counter = Counter(history)
        top_two = [num for num, _ in counter.most_common(4)]
        top_values = [ball_dict[i] for i in top_two]

        final_balls = top_two
        final_values = top_values
        total = sum(final_values)
        avg = total / len(final_values)
        result_bid = int(avg * bid_rate)

        # 전체 결과 텍스트 출력
        full_text = "[공 배치]\n"
        for i in range(1, 16):
            full_text += "{}번 공 → {:,} 원\n".format(i, ball_dict[i])

        full_text += "\n[선택된 공 번호 및 금액]\n"
        for i in selected_balls:
            full_text += "- {}번 공: {:,} 원\n".format(i, ball_dict[i])

        full_text += "\n[자동 추첨 공 번호 및 횟수]\n"
        for i in top_two:
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




# 선택된 공 2개와 랜덤 2개를 포함해서 다시 랜덤을 해서 가장 많이 나온 숫자 4개를 뽑기





#==========================================================================================================================================================================

import random


def generate_ball_dict(base, percent, order):
    min_value = base * (1 - percent / 100)
    max_value = base * (1 + percent / 100)
    mid_index = 7  # 8번 공 위치 (기준값 자리)

    values = [0] * 15
    values[0] = round(min_value)        # 1번 공 = 최소값
    values[mid_index] = round(base)     # 8번 공 = 기초금액액
    values[14] = round(max_value)       # 15번 공 = 최대값

    noise_ratio = 0.7  # 🎯 더 좁은 분포로: n% noise 적용

    # 왼쪽 구간: 2~7번 (index 1~6)
    step_left = (base - min_value) / 7
    for i in range(1, mid_index):
        clean_value = min_value + step_left * i
        noise = random.uniform(-step_left * noise_ratio, step_left * noise_ratio)
        values[i] = round(clean_value + noise)

    # 오른쪽 구간: 9~14번 (index 8~13)
    step_right = (max_value - base) / 7
    for i in range(mid_index + 1, 14):
        clean_value = base + step_right * (i - mid_index)
        noise = random.uniform(-step_right * noise_ratio, step_right * noise_ratio)
        values[i] = round(clean_value + noise)

    # 공 배치를 내림차순으로 정렬하고 싶다면
    if order == 'desc':
        values.reverse()  # 리스트 뒤집기

    # 공 번호 매핑 (1번부터 15번까지)
    ball_dict = {i + 1: values[i] for i in range(15)}
    return ball_dict



1번 공 → 97,000,000 원
2번 공 → 97,428,423 원
3번 공 → 97,856,562 원
4번 공 → 98,286,744 원
5번 공 → 98,715,314 원
6번 공 → 99,142,828 원
7번 공 → 99,571,151 원
8번 공 → 100,000,000 원





