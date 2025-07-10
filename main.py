import os
import time
import hmac
import base64
import requests
import json
from dotenv import load_dotenv

load_dotenv()

# API 환경 변수 로드
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
    requests.post(url, json={"chat_id": TG_USER_ID, "text": message})

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
    response = requests.get(BASE_URL + path + query, headers=headers)
    try:
        return float(response.json()["data"][0]["available"])
    except:
        return 0.0

def get_rsi(symbol="BTCUSDT", interval="1m", limit=100):
    url = f"https://api.bitget.com/api/spot/v1/market/candles?symbol={symbol}&period={interval}&limit={limit}"
    response = requests.get(url)
    closes = [float(kline[4]) for kline in response.json()["data"]]
    if len(closes) < 15:
        return None
    gains = []
    losses = []
    for i in range(1, 8):
        change = closes[-i] - closes[-i - 1]
        if change > 0:
            gains.append(change)
        else:
            losses.append(abs(change))
    avg_gain = sum(gains) / 7
    avg_loss = sum(losses) / 7
    rs = avg_gain / avg_loss if avg_loss != 0 else 100
    rsi = 100 - (100 / (1 + rs))
    return rsi

def enter_position(side="open_long", size=10):
    timestamp = str(int(time.time() * 1000))
    method = "POST"
    path = "/api/mix/v1/order/placeOrder"
    body = {
        "symbol": "BTCUSDT",
        "marginCoin": "USDT",
        "size": str(size),
        "price": "",
        "side": side,
        "orderType": "market",
        "productType": "USDT_PERPETUAL"
    }
    body_json = json.dumps(body)
    signature = generate_signature(timestamp, method, path, "", body_json)
    headers = {
        "ACCESS-KEY": API_KEY,
        "ACCESS-SIGN": signature,
        "ACCESS-TIMESTAMP": timestamp,
        "ACCESS-PASSPHRASE": API_PASSPHRASE,
        "Content-Type": "application/json"
    }
    response = requests.post(BASE_URL + path, headers=headers, data=body_json)
    send_telegram_message(f"🚀 포지션 진입 ({side}) 결과: {response.text}")
    return response.status_code == 200

def run_astral_loop():
    send_telegram_message("🌌 [ASTRAL_EXEC ∞] 루프 시작됨.")
    while True:
        rsi = get_rsi()
        balance = get_balance()
        if rsi is None:
            time.sleep(60)
            continue

        if balance < 10:
            send_telegram_message("⚠️ 잔고 부족. 루프 일시 정지.")
            break

        size = round(balance * 0.9)  # 90%로 거래

        if rsi < 25:
            enter_position("open_long", size)
        elif rsi > 75:
            enter_position("open_short", size)
        else:
            print(f"RSI {rsi:.2f} → 조건 미충족")

        time.sleep(60)

if __name__ == "__main__":
    run_astral_loop()
