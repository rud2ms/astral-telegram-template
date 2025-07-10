import requests
import time
import hmac
import hashlib
import os

# 비트겟 API 키
API_KEY = os.getenv("API_KEY")
SECRET_KEY = os.getenv("SECRET_KEY")
PASSPHRASE = os.getenv("PASSPHRASE")

# 텔레그램
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    data = {"chat_id": CHAT_ID, "text": message}
    requests.post(url, data=data)

def get_timestamp():
    return str(int(time.time() * 1000))

def sign_request(timestamp, method, request_path, body=""):
    message = timestamp + method.upper() + request_path + body
    signature = hmac.new(SECRET_KEY.encode('utf-8'), message.encode('utf-8'), hashlib.sha256).hexdigest()
    return signature

def get_usdt_balance():
    timestamp = get_timestamp()
    method = "GET"
    request_path = "/api/mix/v1/account/accounts?productType=USDT-FUTURES"
    url = "https://api.bitget.com" + request_path
    headers = {
        "ACCESS-KEY": API_KEY,
        "ACCESS-SIGN": sign_request(timestamp, method, request_path),
        "ACCESS-TIMESTAMP": timestamp,
        "ACCESS-PASSPHRASE": PASSPHRASE,
        "Content-Type": "application/json"
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        total = float(data['data'][0]['marginBalance'])
        return total
    else:
        send_telegram_message(f"[오류] 잔고 조회 실패: {response.text}")
        return 0

# 루프 실행 (60분마다 반복)
while True:
    balance = get_usdt_balance()
    if balance > 0:
        send_telegram_message(f"[ASTRAL] 현재 잔고: {balance} USDT")
    time.sleep(3600)
