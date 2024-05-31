import tkinter as tk
from tkinter import ttk, messagebox
import time
from datetime import datetime, timedelta
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import WebDriverException
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

    def safety(func, n=50):
        for _ in range(n):
            try:
                func()
                return
            except WebDriverException:
                time.sleep(0.1)
            except Exception:
                time.sleep(0.1)

        raise WebDriverException

    month = nowtime.month
    day = nowtime.day
    next_date = nowtime + timedelta(days=1)
    next_month = next_date.month
    next_day = next_date.day
    title = f"{month}/{day}_CIEN 사용신청입니다."
    content = f"""
    동아리명: CIEN
    사용 날짜 및 시간: {next_month}월 {next_day}일 00시~07시
    담당자 명 및 인원: {writer} 외 {people}인
    사유: {reason}"""

    # 1. 웹사이트 접속
    driver.get(url)
    # time.sleep(3)

    # 검사
    # already = web.uncertain(lambda: web.find(tag="span", name="Seats"))
    already = driver.find_elements(
        By.XPATH,
        f"//div[contains(@class, 'li_board')]//*[contains(text(), 'CIEN') and contains(text(), {month}) and contains(text(), {day})]",
    )
    if already:
        messagebox.showinfo("정보", "오늘은 이미 작성했습니다!")

    else:
        # 2. 글쓰기 버튼 클릭
        """safety(
            lambda: find(
                '//*[@id="w2022041811317f78559a9"]/div/div[2]/div[3]/div[2]/a'
            ).click()
        )"""
        # time.sleep(1)

        # 3. writer 입력 채우기
        safety(
            lambda: find(
                '//*[@id="post_form"]/div[2]/div/div[2]/div[2]/div[1]/div[2]/span[1]/input'
            ).send_keys(writer)
        )

        # 4. 비밀번호 입력 채우기
        find(
            '//*[@id="post_form"]/div[2]/div/div[2]/div[2]/div[1]/div[2]/span[2]/input'
        ).send_keys(pw)

        # 5. 제목 입력 채우기
        find('//*[@id="post_subject"]').clear()
        find('//*[@id="post_subject"]').send_keys(title)

        # 6. 본문 내용 채우기
        find('//*[@id="post_body"]/div[1]/div').clear()
        find('//*[@id="post_body"]/div[1]/div').send_keys(content)

        # (전송)
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
        url="https://cauclub.co.kr/reports/?q=YToxOntzOjEyOiJrZXl3b3JkX3R5cGUiO3M6MzoiYWxsIjt9&board=b20220418b496dcf2b8ae2&bmode=write&back_url=L3JlcG9ydHM%3D",
        writer=writer,
        people=people,
        pw=14789,
        reason=reason,
        nowtime=datetime.now(),
    )

    # messagebox.showinfo("정보", "양식 제출이 완료되었습니다!")


def show_help():
    help_text = """<동아리방 야간 사용 신청 프로그램 ver 1.1>
- 뭐 입력 안 하고 제출하면 기본값으로 작성
- 값 입력 시 해당값으로 작성
- 인터넷 너무 느리면 잘 안 될 수도 있음
- 문제 시 삭제
- 비밀번호는 국룰 다섯자리 숫자"""
    messagebox.showinfo("도움말", help_text)


app = tk.Tk()
app.title("동아리 야간 신청")
app.geometry("400x220")
app.resizable(False, False)

frame = ttk.Frame(app, padding="10 10 10 10")
frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

frame.columnconfigure(0, weight=1)
frame.columnconfigure(1, weight=1)
frame.rowconfigure(4, minsize=30)

ttk.Label(frame, text="글쓴이 (기본값: 이기석)").grid(
    row=1, column=0, sticky=tk.W, pady=5
)
ttk.Label(frame, text="인원수 (기본값: 2)").grid(row=2, column=0, sticky=tk.W, pady=5)
ttk.Label(frame, text="야간 신청 이유 (기본값: 랜덤)").grid(
    row=3, column=0, sticky=tk.W, pady=5
)

writer_var = tk.StringVar()
people_var = tk.StringVar()
reason_var = tk.StringVar()


help_button = ttk.Button(frame, text="도움말", command=show_help)
help_button.grid(row=0, column=1, sticky=(tk.E))

writer_entry = ttk.Entry(frame, textvariable=writer_var, width=30)
writer_entry.grid(row=1, column=1, pady=5)

people_entry = ttk.Entry(frame, textvariable=people_var, width=30)
people_entry.grid(row=2, column=1, pady=5)

reason_entry = ttk.Entry(frame, textvariable=reason_var, width=30)
reason_entry.grid(row=3, column=1, pady=5)

submit_button = ttk.Button(frame, text="제출", command=submit_form)
submit_button.grid(
    row=4, columnspan=2, ipady=5, ipadx=5, pady=10, sticky=(tk.W, tk.E, tk.W)
)


ttk.Label(
    frame,
    text="제작자: 주황폰트, 곽아만, 야릇한미디움레어",
    font=("Helvetica", 9, "italic"),
).grid(row=5, column=0, columnspan=2, pady=5, sticky=tk.E)

print("""<ver 1.1>
- UI 개선
- 텍스트 박스 추가
- 안정성 개선
<ver 1.2>
- 이미 작성된 글 확인 과정 스킵(임시)
- 사용 날짜가 다음 날 기준으로 작성되도록 수정""")
app.mainloop()
