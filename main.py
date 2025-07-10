import time
import requests
import hmac
import hashlib
import os
from dotenv import load_dotenv

# .env 파일 로드
load_dotenv()

API_KEY = os.getenv("API_KEY")
API_SECRET = os.getenv("API_SECRET")
PASSPHRASE = os.getenv("PASSPHRASE")

BOT_TOKEN = os.getenv("BOT_TOKEN")
USER_ID = os.getenv("USER_ID")

def send_telegram(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": USER_ID,
        "text": message
    }
    try:
        requests.post(url, json=payload)
    except Exception as e:
        print("텔레그램 전송 오류:", e)

def generate_signature(timestamp, method, request_path, body):
    message = f"{timestamp}{method}{request_path}{body}"
    mac = hmac.new(
        bytes(API_SECRET, encoding='utf-8'),
        bytes(message, encoding='utf-8'),
        digestmod=hashlib.sha256
    )
    return mac.hexdigest()

def get_balance():
    request_path = "/api/mix/v1/account/accounts?productType=USDT-FUTURES"
    method = "GET"
    body = ""
    timestamp = str(int(time.time() * 1000))
    signature = generate_signature(timestamp, method, request_path, body)

    headers = {
        "ACCESS-KEY": API_KEY,
        "ACCESS-SIGN": signature,
        "ACCESS-TIMESTAMP": timestamp,
        "ACCESS-PASSPHRASE": PASSPHRASE,
        "Content-Type": "application/json"
    }

    url = "https://api.bitget.com" + request_path
    response = requests.get(url, headers=headers)

    try:
        data = response.json()
        usdt_balance = float(data['data'][0]['available'])
        return usdt_balance
    except Exception as e:
        print("잔고 조회 실패:", response.text)
        send_telegram(f"[오류] 잔고 조회 실패: {response.text}")
        return 0

# === 루프 시작 ===
send_telegram("🚀 ASTRAL EXEC 전략 루프 시작됨")

balance = get_balance()
print(f"현재 잔고: {balance} USDT")

if balance > 1:
    send_telegram(f"✅ 전략 실행 조건 만족! 잔고: {balance} USDT")
    # 여기에 실제 전략 실행 코드 삽입 가능
else:
    send_telegram(f"⚠️ 현재 잔고 부족 또는 오류. {balance} USDT")
