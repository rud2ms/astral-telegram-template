import requests
import time
import hmac
import hashlib
import os

# 환경변수에서 불러오기
API_KEY = os.getenv("API_KEY")
SECRET_KEY = os.getenv("SECRET_KEY")
PASSPHRASE = os.getenv("PASSPHRASE")
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    data = {"chat_id": CHAT_ID, "text": message}
    try:
        requests.post(url, data=data)
    except Exception as e:
        print(f"텔레그램 전송 오류: {e}")

def get_timestamp():
    return str(int(time.time() * 1000))

def sign_request(timestamp, method, request_path, body=""):
    message = f"{timestamp}{method.upper()}{request_path}{body}"
    signature = hmac.new(SECRET_KEY.encode(), message.encode(), hashlib.sha256).hexdigest()
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

    try:
        response = requests.get(url, headers=headers)
        res_json = response.json()
        if res_json.get("code") == "00000":
            balance = res_json["data"][0]["marginBalance"]
            return float(balance)
        else:
            send_telegram_message(f"[오류] 잔고 조회 실패: {res_json.get('msg')}")
            return None
    except Exception as e:
        send_telegram_message(f"[예외] 잔고 조회 중 오류 발생: {e}")
        return None

# 루프 실행
if __name__ == "__main__":
    while True:
        balance = get_usdt_balance()
        if balance is not None:
            send_telegram_message(f"[ASTRAL_EXEC] 현재 잔고: {balance} USDT")
        time.sleep(3600)
