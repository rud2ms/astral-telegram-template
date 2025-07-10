import requests
import time
import hmac
import hashlib
import os
from dotenv import load_dotenv

# 환경 변수 불러오기
load_dotenv()

# 비트겟 API 정보
api_key = os.getenv("API_KEY")
secret_key = os.getenv("SECRET_KEY")
passphrase = os.getenv("PASSPHRASE")

# 텔레그램 설정
telegram_token = os.getenv("TELEGRAM_TOKEN")
chat_id = os.getenv("CHAT_ID")

def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{telegram_token}/sendMessage"
    data = {"chat_id": chat_id, "text": message}
    requests.post(url, data=data)

def sign_request(timestamp, method, request_path, body=""):
    message = f'{timestamp}{method.upper()}{request_path}{body}'
    signature = hmac.new(secret_key.encode('utf-8'),
                         message.encode('utf-8'),
                         hashlib.sha256).hexdigest()
    return signature

def get_headers(method, request_path, body=""):
    timestamp = str(int(time.time() * 1000))
    signature = sign_request(timestamp, method, request_path, body)
    headers = {
        'ACCESS-KEY': api_key,
        'ACCESS-SIGN': signature,
        'ACCESS-TIMESTAMP': timestamp,
        'ACCESS-PASSPHRASE': passphrase,
        'Content-Type': 'application/json'
    }
    return headers

def get_usdt_balance():
    method = "GET"
    request_path = "/api/mix/v1/account/accounts?productType=USDT-FUTURES"
    url = "https://api.bitget.com" + request_path
    headers = get_headers(method, request_path)
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        balance = data['data'][0]['marginBalance']
        send_telegram_message(f"[ASTRAL] 현재 잔고는 {balance} USDT입니다.")
    else:
        send_telegram_message(f"[오류] 잔고 조회 실패: {response.text}")

# 실행
get_usdt_balance()
