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

def generate_signature(timestamp, method, path, query_string="", body=""):
    message = f"{timestamp}{method}{path}{query_string}{body}"
    mac = hmac.new(API_SECRET.encode(), message.encode(), digestmod="sha256")
    return base64.b64encode(mac.digest()).decode()

def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TG_TOKEN}/sendMessage"
    data = {"chat_id": TG_USER_ID, "text": message}
    try:
        requests.post(url, json=data)
    except Exception as e:
        print("텔레그램 전송 실패:", e)

def get_balance():
    timestamp = str(int(time.time() * 1000))
    method = "GET"
    path = "/api/mix/v1/account/accounts"
    query = "?productType=USDT_PERPETUAL"
    signature = generate_signature(timestamp, method, path, query)

    headers = {
        "ACCESS-KEY": API_KEY,
        "ACCESS-SIGN": signature,
        "ACCESS-TIMESTAMP": timestamp,
        "ACCESS-PASSPHRASE": API_PASSPHRASE,
        "Content-Type": "application/json"
    }

    url = BASE_URL + path + query
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        try:
            return float(response.json()['data'][0]['available'])
        except:
            return 0.0
    else:
        print("잔고 조회 실패:", response.text)
        return 0.0

def enter_trade():
    print("🚀 [진입] 조건 충족 - 실제 거래 실행")
    send_telegram_message("🚨 거래 진입 실행됨 (테스트용 메시지)")

def run_strategy_loop():
    send_telegram_message("🌌 ASTRAL_EXEC 전략 루프 시작")
    balance = get_balance()
    if balance > 0:
        send_telegram_message(f"✅ 잔고: {balance} USDT")
        enter_trade()
    else:
        send_telegram_message("⚠️ 잔고 부족 또는 조회 실패")
    send_telegram_message("✅ 전략 루프 종료")

if __name__ == "__main__":
    run_strategy_loop()
