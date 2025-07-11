import os
import time
import hmac
import base64
import requests
from dotenv import load_dotenv

load_dotenv()

# 환경변수 로딩
API_KEY = os.getenv("API_KEY")
API_SECRET = os.getenv("API_SECRET")
API_PASSPHRASE = os.getenv("API_PASSPHRASE")
PRODUCT_TYPE = os.getenv("PRODUCT_TYPE")  # 이 부분이 핵심!
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
    query = f"?productType={PRODUCT_TYPE}"  # 여기도 반드시 포함돼야 함
    request_path = path + query
    url = BASE_URL + request_path

    signature = generate_signature(timestamp, method, path, query)

    headers = {
        "ACCESS-KEY": API_KEY,
        "ACCESS-SIGN": signature,
        "ACCESS-TIMESTAMP": timestamp,
        "ACCESS-PASSPHRASE": API_PASSPHRASE,
        "Content-Type": "application/json"
    }

    try:
        response = requests.get(url, headers=headers)
        data = response.json()
        usdt_balance = float(data['data'][0]['available'])
        return usdt_balance
    except Exception as e:
        print("잔고 조회 실패:", e)
        return 0.0

def enter_trade():
    print("🚨 실거래 진입: enter_trade() 호출됨")
    # 여기에 실제 포지션 진입 로직 구현 예정

def run_strategy_loop():
    send_telegram_message("🚀 ASTRAL EXEC 전략 루프 시작됨")
    balance = get_balance()

    if balance > 0:
        send_telegram_message(f"✅ 현재 잔고: {balance} USDT")
        enter_trade()
    else:
        send_telegram_message("⚠️ 잔고 부족 또는 조회 실패")
    
    send_telegram_message("✅ 전략 루프 종료됨")

if __name__ == "__main__":
    run_strategy_loop()
