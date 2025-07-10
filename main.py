import requests
import time
import hmac
import hashlib
from datetime import datetime

# Bitget API 설정
API_KEY = "bg_47e6906b4c0a577ea0ef03c707b5a601"
SECRET_KEY = "d5d677354d0edc9c18fa8bcbcdc59668a7e5d04e6d6121017b3ee5974bea2a64"
PASSPHRASE = "sodlfmaruddms1"

# Telegram 설정
TELEGRAM_TOKEN = "8121549228:AAH3Yqipscnr5rnsY0eFCDHSATC9FfU9qa0"
CHAT_ID = "7909031883"

# 텔레그램 메시지 전송
def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    data = {"chat_id": CHAT_ID, "text": message}
    requests.post(url, data=data)

# 타임스탬프 생성
def get_timestamp():
    return str(int(time.time() * 1000))

# 서명 생성
def sign_request(timestamp, method, request_path, body=""):
    message = timestamp + method.upper() + request_path + body
    signature = hmac.new(SECRET_KEY.encode('utf-8'), message.encode('utf-8'), hashlib.sha256).hexdigest()
    return signature

# USDT 잔고 조회
def get_usdt_balance():
    timestamp = get_timestamp()
    method = "GET"
    request_path = "/api/mix/v1/account/accounts"
    query_string = "productType=USDT-FUTURES"
    full_url = f"https://api.bitget.com{request_path}?{query_string}"
    body = f"?{query_string}"

    headers = {
        "ACCESS-KEY": API_KEY,
        "ACCESS-SIGN": sign_request(timestamp, method, request_path, body),
        "ACCESS-TIMESTAMP": timestamp,
        "ACCESS-PASSPHRASE": PASSPHRASE,
        "Content-Type": "application/json"
    }

    response = requests.get(full_url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        total = float(data['data'][0]['marginBalance'])
        return total
    else:
        send_telegram_message(f"[오류] 잔고 조회 실패: {response.text}")
        return 0

# 자동 루프 실행 (예: 1시간마다)
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
    time.sleep(3600)  # 1시간마다 실행
