import requests
import time

# 설정
TOKEN = '8121549228:AAH3Yqipscnr5rnsY0eFCDHSATC9FfU9qa0'
CHAT_ID = '7909031883'
TELEGRAM_API_URL = f"https://api.telegram.org/bot{TOKEN}/sendMessage"

def send_message(text):
    data = {'chat_id': CHAT_ID, 'text': text}
    requests.post(TELEGRAM_API_URL, data=data)

def run_strategy():
    # 자동화 루프 예시 (테스트용)
    send_message("🚀 ASTRAL EXEC 전략 루프 시작됨")
    
    # 예시 전략 실행
    for i in range(3):
        send_message(f"루프 실행 중: Step {i+1}")
        time.sleep(1)

    send_message("✅ 전략 루프 종료됨")
