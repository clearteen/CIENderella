import tkinter as tk
from tkinter import ttk, messagebox
import time
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
import random


def get_random_reason():
    reasons = [
        "게임 공모전 준비",
        "게임 분석 스터디",
        "게임 분석 스터디",
        "유니티 코딩 실습",
        "게임 기획 스터디 준비",
        "언리얼 코딩 실습",
        "게임 분석 활동",
        "기획서 문서 작업",
    ]
    return random.choice(reasons)


def run_submit_form(driver, url, writer, pw, people, reason, nowtime):
    def find(xpath):
        return driver.find_element(By.XPATH, xpath)

    month = nowtime.month
    day = nowtime.day
    title = f"{month}/{day}_CIEN 사용신청입니다."
    content = f"""
    동아리명: CIEN
    사용 날짜 및 시간: {month}월 {day}일 00시~07시
    담당자 명 및 인원: {writer} 외 {people}인
    사유: {reason}"""

    driver.get(url)
    time.sleep(3)

    already = driver.find_elements(
        By.XPATH,
        "//div[contains(@class, 'li_board')]//*[contains(text(), 'CIEN') and contains(text(), '28')]",
    )
    if already:
        print("already!")
        messagebox.showinfo("정보", "오늘은 이미 작성했습니다!")
    else:
        print("pass")
        find('//*[@id="w2022041811317f78559a9"]/div/div[2]/div[3]/div[2]/a').click()
        time.sleep(1)
        find(
            '//*[@id="post_form"]/div[2]/div/div[2]/div[2]/div[1]/div[2]/span[1]/input'
        ).send_keys(writer)
        find(
            '//*[@id="post_form"]/div[2]/div/div[2]/div[2]/div[1]/div[2]/span[2]/input'
        ).send_keys(pw)
        find('//*[@id="post_subject"]').clear()
        find('//*[@id="post_subject"]').send_keys(title)
        find('//*[@id="post_body"]/div[1]/div').clear()
        find('//*[@id="post_body"]/div[1]/div').send_keys(content)
        # find('//*[@id="board_container"]/div[1]/div/div[2]/button').click()


def submit_form():
    writer = writer_var.get() or "이기석"
    people_input = people_var.get()
    people = int(people_input) if people_input.isdigit() else 2
    reason = reason_var.get() or get_random_reason()

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_experimental_option("detach", True)
    driver = webdriver.Chrome(options=chrome_options)

    run_submit_form(
        driver,
        url="https://cauclub.co.kr/reports",
        writer=writer,
        people=people,
        pw=14789,
        reason=reason,
        nowtime=datetime.now(),
    )

    messagebox.showinfo("정보", "양식 제출이 완료되었습니다!")


app = tk.Tk()
app.title("동아리 야간 신청")
app.geometry("400x250")
app.resizable(False, False)

frame = ttk.Frame(app, padding="10 10 10 10")
frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

frame.columnconfigure(0, weight=1)
frame.columnconfigure(1, weight=1)

ttk.Label(frame, text="글쓴이 (기본값: 이기석)").grid(
    row=0, column=0, sticky=tk.W, pady=5
)
ttk.Label(frame, text="인원수 (기본값: 2)").grid(row=1, column=0, sticky=tk.W, pady=5)
ttk.Label(frame, text="야간 신청 이유 (기본값: 랜덤)").grid(
    row=2, column=0, sticky=tk.W, pady=5
)

writer_var = tk.StringVar()
people_var = tk.StringVar()
reason_var = tk.StringVar()

writer_entry = ttk.Entry(frame, textvariable=writer_var, width=30)
writer_entry.grid(row=0, column=1, pady=5)

people_entry = ttk.Entry(frame, textvariable=people_var, width=30)
people_entry.grid(row=1, column=1, pady=5)

reason_entry = ttk.Entry(frame, textvariable=reason_var, width=30)
reason_entry.grid(row=2, column=1, pady=5)

submit_button = ttk.Button(frame, text="제출", command=submit_form)
submit_button.grid(row=3, column=1, pady=20, sticky=(tk.W, tk.E))

ttk.Label(frame, text="제작자: 주황폰트 외 1명", font=("Helvetica", 9, "italic")).grid(
    row=4, column=0, columnspan=2, pady=10, sticky=tk.E
)
print("비밀번호는 다섯 자리")
print("엔터 후 실행")
app.mainloop()
