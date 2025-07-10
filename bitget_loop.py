import requests
import time
import hmac
import hashlib
from datetime import datetime

# 비트겟 API 키
API_KEY = "bg_47e6906b4c0a577ea0ef03c707b5a601"
SECRET_KEY = "d5d677354d0edc9c18fa8bcbcdc59668a7e5d04e6d6121017b3ee5974bea2a64"
PASSPHRASE = "sodlfmaruddms1"

# 텔레그램 설정
TELEGRAM_TOKEN = "8121549228:AAH3Yqipscnr5rnsY0eFCDHSATC9FfU9qa0"
CHAT_ID = "7909031883"

def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    data = {"chat_id": CHAT_ID, "text": message}
    try:
        requests.post(url, data=data)
    except Exception as e:
        print("텔레그램 오류:", e)

def get_timestamp():
    return str(int(time.time() * 1000))

def sign_request(timestamp, method, request_path, body=""):
    pre_hash = f"{timestamp}{method.upper()}{request_path}{body}"
    signature = hmac.new(SECRET_KEY.encode('utf-8'), pre_hash.encode('utf-8'), hashlib.sha256).hexdigest()
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
        try:
            data = response.json()
            total = float(data['data'][0]['marginBalance'])
            send_telegram_message(f"[ASTRAL] 현재 잔고는 {total} USDT입니다.")
            return total
        except Exception as e:
            send_telegram_message(f"[ASTRAL 오류] 응답 파싱 오류: {str(e)}")
    else:
        send_telegram_message(f"[ASTRAL 오류] 잔고 조회 실패: {response.status_code} - {response.text}")
    return 0

# 메인 루프
while True:
    get_usdt_balance()
    time.sleep(3600)  # 1시간마다 실행
