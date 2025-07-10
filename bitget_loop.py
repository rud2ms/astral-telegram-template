import requests
import time
import hmac
import hashlib
import json

# 비트겟 API 키
API_KEY = "bg_80625110d7152ca34ef7b5a63d0a1e9c"
SECRET_KEY = "47c8862d0c869f978d06deaa95f08ca4aff54c74f9a71bd84a53d27412a2ed14"
PASSPHRASE = "sodlfmaruddms1"

# 텔레그램 설정
TELEGRAM_TOKEN = "8121549228:AAH3Yqipscnr5rnsY0eFCDHSATC9FfU9qa0"
CHAT_ID = "7909031883"

def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    data = {"chat_id": CHAT_ID, "text": message}
    requests.post(url, data=data)

def get_timestamp():
    return str(int(time.time() * 1000))

def sign_request(timestamp, method, request_path, body=""):
    message = f"{timestamp}{method.upper()}{request_path}{body}"
    signature = hmac.new(SECRET_KEY.encode(), message.encode(), hashlib.sha256).hexdigest()
    return signature

def get_usdt_balance():
    timestamp = get_timestamp()
    method = "GET"
    request_path = "/api/mix/v1/account/accounts?productType=USDT-FUTURES"
    full_url = f"https://api.bitget.com{request_path}"
    body = ""

    headers = {
        "ACCESS-KEY": API_KEY,
        "ACCESS-SIGN": sign_request(timestamp, method, request_path, body),
        "ACCESS-TIMESTAMP": timestamp,
        "ACCESS-PASSPHRASE": PASSPHRASE,
        "Content-Type": "application/json"
    }

    response = requests.get(full_url, headers=headers)
    
    if response.status_code == 200:
        try:
            data = response.json()
            total = float(data['data'][0]['marginBalance'])
            return total
        except Exception as e:
            send_telegram_message(f"[ASTRAL 오류] JSON 파싱 실패: {str(e)}")
            return 0
    else:
        send_telegram_message(f"[ASTRAL 오류] 잔고 조회 실패: {response.status_code} - {response.text}")
        return 0

# 실행 루프
while True:
    send_telegram_message("🚀 ASTRAL EXEC 전략 루프 시작됨")

    for step in range(1, 4):
        send_telegram_message(f"루프 실행 중: Step {step}")
        time.sleep(1)

    balance = get_usdt_balance()
    if balance > 1:
        send_telegram_message(f"✅ 잔고: {balance} USDT")
    else:
        send_telegram_message(f"⚠️ 현재 잔고 부족 또는 오류. {balance} USDT")

    send_telegram_message("✅ 전략 루프 종료됨\n")
    time.sleep(3600)
