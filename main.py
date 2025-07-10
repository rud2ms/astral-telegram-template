import os
import time
import hmac
import base64
import requests
import statistics
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("API_KEY")
API_SECRET = os.getenv("API_SECRET")
API_PASSPHRASE = os.getenv("API_PASSPHRASE")
TG_TOKEN = os.getenv("TG_TOKEN")
TG_USER_ID = os.getenv("TG_USER_ID")
BASE_URL = "https://api.bitget.com"

SYMBOL = "BTCUSDT"
PRODUCT_TYPE = "USDT_PERPETUAL"

# 서명 생성
def generate_signature(timestamp, method, request_path, query_string="", body=""):
    message = f"{timestamp}{method}{request_path}{query_string}{body}"
    mac = hmac.new(API_SECRET.encode(), message.encode(), digestmod="sha256")
    return base64.b64encode(mac.digest()).decode()

# 텔레그램 알림
def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TG_TOKEN}/sendMessage"
    data = {"chat_id": TG_USER_ID, "text": message}
    try:
        requests.post(url, json=data)
    except Exception as e:
        print("텔레그램 전송 실패:", e)

# RSI 계산
def calculate_rsi(closes, period=14):
    if len(closes) < period + 1:
        return None
    gains = []
    losses = []
    for i in range(1, period + 1):
        delta = closes[-i] - closes[-i - 1]
        if delta >= 0:
            gains.append(delta)
        else:
            losses.append(abs(delta))
    avg_gain = statistics.mean(gains) if gains else 0
    avg_loss = statistics.mean(losses) if losses else 0
    if avg_loss == 0:
        return 100
    rs = avg_gain / avg_loss
    return 100 - (100 / (1 + rs))

# 실시간 RSI 데이터 요청
def get_rsi():
    url = f"{BASE_URL}/api/mix/v1/market/candles?symbol={SYMBOL}&granularity=1m&limit=100"
    try:
        response = requests.get(url)
        candles = response.json().get("data")
        if not candles:
            print("⚠️ 캔들 데이터 없음")
            return None
        closes = [float(kline[4]) for kline in candles]
        return calculate_rsi(closes)
    except Exception as e:
        print("RSI 계산 실패:", e)
        return None

# 잔고 조회
def get_balance():
    timestamp = str(int(time.time() * 1000))
    method = "GET"
    path = "/api/mix/v1/account/accounts"
    query_string = f"?productType={PRODUCT_TYPE}"
    url = BASE_URL + path + query_string
    signature = generate_signature(timestamp, method, path, query_string)
    headers = {
        "ACCESS-KEY": API_KEY,
        "ACCESS-SIGN": signature,
        "ACCESS-TIMESTAMP": timestamp,
        "ACCESS-PASSPHRASE": API_PASSPHRASE,
        "Content-Type": "application/json"
    }
    response = requests.get(url, headers=headers)
    try:
        data = response.json()
        return float(data["data"][0]["available"])
    except:
        print("잔고 조회 실패:", response.text)
        return 0.0

# 진입 전략
def enter_trade():
    print("🚨 진입 시도 중... (모의 실행)")
    # 실거래 주문 로직은 여기에 추가

# 전략 루프
def run_astral_loop():
    send_telegram_message("🚀 ASTRAL EXEC 전략 루프 시작")
    balance = get_balance()
    rsi = get_rsi()

    if rsi is None:
        send_telegram_message("⚠️ RSI 계산 실패. 전략 중단")
        return

    send_telegram_message(f"📊 현재 RSI: {rsi:.2f}")

    if balance <= 0:
        send_telegram_message("❌ 잔고 없음. 전략 종료")
        return

    if rsi < 30:
        send_telegram_message(f"🟢 RSI {rsi:.2f} → 진입 조건 충족")
        enter_trade()
    else:
        send_telegram_message(f"🕒 RSI {rsi:.2f} → 대기")

    send_telegram_message("✅ 전략 루프 종료")

if __name__ == "__main__":
    run_astral_loop()
