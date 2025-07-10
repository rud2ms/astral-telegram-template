import os
import time
import hmac
import base64
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("API_KEY")
API_SECRET = os.getenv("API_SECRET")
API_PASSPHRASE = os.getenv("API_PASSPHRASE")
TG_TOKEN = os.getenv("TG_TOKEN")
TG_USER_ID = os.getenv("TG_USER_ID")
BASE_URL = "https://api.bitget.com"

def generate_signature(timestamp, method, request_path, query_string, body=""):
    message = f"{timestamp}{method}{request_path}{query_string}{body}"
    mac = hmac.new(API_SECRET.encode(), message.encode(), digestmod="sha256")
    return base64.b64encode(mac.digest()).decode()

def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TG_TOKEN}/sendMessage"
    data = {
        "chat_id": TG_USER_ID,
        "text": message
    }
    try:
        requests.post(url, json=data)
    except Exception as e:
        print("텔레그램 전송 실패:", e)

def get_balance():
    timestamp = str(int(time.time() * 1000))
    method = "GET"
    path = "/api/mix/v1/account/accounts"
    query_string = "?productType=USDT_PERPETUAL"
    request_path = path + query_string
    url = BASE_URL + request_path

    signature = generate_signature(timestamp, method, path, query_string)

    headers = {
        "ACCESS-KEY": API_KEY,
        "ACCESS-SIGN": signature,
        "ACCESS-TIMESTAMP": timestamp,
        "ACCESS-PASSPHRASE": API_PASSPHRASE,
        "Content-Type": "application/json"
    }

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        try:
            data = response.json()
            usdt_balance = float(data['data'][0]['available'])
            return usdt_balance
        except Exception as e:
            print("잔고 파싱 오류:", e)
            return 0.0
    else:
        print("잔고 조회 실패:", response.text)
        return 0.0

def run_strategy_loop():
    send_telegram_message("🚀 ASTRAL EXEC 전략 루프 시작됨")
    print("루프 실행 중: Step 1")
    print("루프 실행 중: Step 2")
    print("루프 실행 중: Step 3")

    balance = get_balance()
    if balance > 0:
        send_telegram_message(f"✅ 현재 잔고: {balance} USDT")
    else:
        send_telegram_message("⚠️ 현재 잔고 부족 또는 오류. 0 USDT")

    send_telegram_message("✅ 전략 루프 종료됨")

if __name__ == "__main__":
    run_strategy_loop()
    enter_trade()  # ✅ 실거래 진입 함수
