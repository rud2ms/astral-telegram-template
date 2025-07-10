import requests
import time
import hmac
import hashlib
import json

# 비트겟 API 키
API_KEY = "bg_80625110d7152ca34ef7b5a63d0a1e9c"
SECRET_KEY = "47c8862d0c869f978d06deaa95f08ca4aff54c74f9a71bd84a53d27412a2ed14"
PASSPHRASE = "sodlfmaruddms1"

# 텔레그램
TELEGRAM_TOKEN = "8121549228:AAH3Yqipscnr5rnsY0eFCDHSATC9FfU9qa0"
CHAT_ID = "7909031883"

def send_telegram_message(msg):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    data = {"chat_id": CHAT_ID, "text": msg}
    requests.post(url, data=data)

def get_timestamp():
    return str(int(time.time() * 1000))

def sign_request(timestamp, method, request_path, body=""):
    message = f"{timestamp}{method.upper()}{request_path}{body}"
    signature = hmac.new(SECRET_KEY.encode('utf-8'), message.encode('utf-8'), hashlib.sha256).hexdigest()
    return signature

def get_usdt_balance():
    timestamp = get_timestamp()
    method = "GET"
    request_path = "/api/mix/v1/account/accounts?productType=USDT-FUTURES"
    url = "https://api.bitget.com" + request_path
    body = ""  # GET 요청은 body가 반드시 빈 문자열이어야 함

    headers = {
        "ACCESS-KEY": API_KEY,
        "ACCESS-SIGN": sign_request(timestamp, method, request_path, body),
        "ACCESS-TIMESTAMP": timestamp,
        "ACCESS-PASSPHRASE": PASSPHRASE,
        "Content-Type": "application/json"
    }

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        balance = float(data['data'][0]['marginBalance'])
        return balance
    else:
        send_telegram_message(f"[ASTRAL 오류] 잔고 조회 실패: {response.status_code} - {response.text}")
        return 0

# 전략 루프
while True:
    send_telegram_message("🚀 ASTRAL EXEC 전략 루프 시작됨")
    send_telegram_message("루프 실행 중: Step 1")
    send_telegram_message("루프 실행 중: Step 2")
    send_telegram_message("루프 실행 중: Step 3")

    balance = get_usdt_balance()

    if balance > 1:
        send_telegram_message(f"✅ 잔고: {balance} USDT")
    else:
        send_telegram_message(f"⚠️ 현재 잔고 부족 또는 오류. {balance} USDT")

    send_telegram_message("✅ 전략 루프 종료됨\n")
    time.sleep(3600)
