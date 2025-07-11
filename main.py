
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

def generate_signature(timestamp, method, request_path, query_string="", body=""):
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
    query_params = {"productType": "USDT_PERPETUAL"}
    url = BASE_URL + path

    signature = generate_signature(timestamp, method, path)

    headers = {
        "ACCESS-KEY": API_KEY,
        "ACCESS-SIGN": signature,
        "ACCESS-TIMESTAMP": timestamp,
        "ACCESS-PASSPHRASE": API_PASSPHRASE,
        "Content-Type": "application/json"
    }

    try:
        response = requests.get(url, headers=headers, params=query_params)
        data = response.json()
        usdt_balance = float(data['data'][0]['available'])
        return usdt_balance
    except Exception as e:
        print("잔고 조회 실패:", e)
        return 0.0

def get_kline(symbol="BTCUSDT_UMCBL", interval="1m", limit=100):
    url = f"{BASE_URL}/api/mix/v1/market/candles"
    params = {
        "symbol": symbol,
        "granularity": "60",  # 1분봉
        "limit": limit
    }
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        return response.json()["data"]
    except Exception as e:
        print("캔들 데이터 요청 실패:", e)
        return []

def calculate_rsi(closes, period=14):
    if len(closes) < period:
        return None
    gains, losses = [], []
    for i in range(1, period + 1):
        delta = closes[i] - closes[i - 1]
        if delta >= 0:
            gains.append(delta)
            losses.append(0)
        else:
            gains.append(0)
            losses.append(-delta)
    avg_gain = sum(gains) / period
    avg_loss = sum(losses) / period
    if avg_loss == 0:
        return 100
    rs = avg_gain / avg_loss
    return 100 - (100 / (1 + rs))

def enter_trade():
    print("🚨 실거래 진입: 조건 충족됨 (RSI)")
    send_telegram_message("🚨 실거래 진입 실행됨")

def run_astral_loop():
    send_telegram_message("🚀 ASTRAL EXEC 전략 루프 시작됨")

    balance = get_balance()
    if balance <= 0:
        send_telegram_message("⚠️ 현재 잔고 부족 또는 조회 실패")
        send_telegram_message("✅ 전략 루프 종료됨")
        return

    kline_data = get_kline()
    if not kline_data:
        send_telegram_message("⚠️ 캔들 데이터 없음. 전략 중단")
        return

    closes = [float(k[4]) for k in kline_data[::-1]]  # 종가
    rsi = calculate_rsi(closes)
    if rsi is None:
        send_telegram_message("⚠️ RSI 계산 실패. 전략 중단")
        return

    send_telegram_message(f"📊 현재 RSI: {rsi:.2f}")
    if rsi < 30:
        enter_trade()
    else:
        send_telegram_message("📉 RSI 기준 미충족. 대기")

    send_telegram_message("✅ 전략 루프 종료됨")

if __name__ == "__main__":
    run_astral_loop()
