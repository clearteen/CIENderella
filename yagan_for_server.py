import tkinter as tk
from tkinter import ttk, messagebox
import time
from datetime import datetime, timedelta
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import WebDriverException
import random
import logging
import os

from getPeople import isPeople

countPeople = isPeople()

# 로그 설정
logging.basicConfig(
    filename="log_file",  # 로그 파일 경로
    level=logging.INFO,  # 로그 수준 설정
    format="%(asctime)s %(levelname)s:%(message)s",  # 로그 메시지 형식
    datefmt="%Y-%m-%d %H:%M:%S",  # 날짜 형식
)


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
    if people > 1:
        who = f"{writer} 외 {people-1}인"
    else:
        who = writer
    content = f"""
    동아리명: CIEN
    사용 날짜 및 시간: {next_month}월 {next_day}일 00시~07시
    담당자 명 및 인원: {who}
    사유: {reason}"""

    # 1. 웹사이트 접속
    driver.get(url)
    # time.sleep(3)

    # 검사
    # already = web.uncertain(lambda: web.find(tag="span", name="Seats"))
    already = driver.find_elements(
        By.XPATH,
        f"//div[contains(@class, 'li_board')]//*[contains(text(), '{title}')]",
    )
    if already:
        logging.info("already")

    else:
        # 2. 글쓰기 버튼 클릭
        """safety(
            lambda: find(
                '//*[@id="w2022041811317f78559a9"]/div/div[2]/div[3]/div[2]/a'
            ).click()
        )"""
        driver.get(
            "https://cauclub.co.kr/reports/?q=YToxOntzOjEyOiJrZXl3b3JkX3R5cGUiO3M6MzoiYWxsIjt9&board=b20220418b496dcf2b8ae2&bmode=write&back_url=L3JlcG9ydHM%3D"
        )
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
        time.sleep(2)

        # 로그 작성
        logging.info(f"countPeople - {countPeople}")

    # 종료
    driver.quit()


def submit_form():
    writer = "김현수"
    people = countPeople
    reason = get_random_reason()

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
        nowtime=datetime.now()
        if datetime.now().hour >= 12
        else datetime.now() - timedelta(days=1),
    )


if isPeople():
    submit_form()
else:
    logging.info("None")
