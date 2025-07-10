
import os
import requests
import time
import hmac
import hashlib

API_KEY = os.getenv("API_KEY")
SECRET_KEY = os.getenv("SECRET_KEY")
PASSPHRASE = os.getenv("PASSPHRASE")

BASE_URL = "https://api.bitget.com"

def get_timestamp():
    return str(int(time.time() * 1000))

def sign_request(timestamp, method, request_path, body=""):
    message = f"{timestamp}{method.upper()}{request_path}{body}"
    signature = hmac.new(SECRET_KEY.encode(), message.encode(), hashlib.sha256).hexdigest()
    return signature

def get_futures_balance():
    path = "/api/mix/v1/account/accounts?productType=USDT-FUTURES"
    timestamp = get_timestamp()
    sign = sign_request(timestamp, "GET", path)

    headers = {
        "ACCESS-KEY": API_KEY,
        "ACCESS-SIGN": sign,
        "ACCESS-TIMESTAMP": timestamp,
        "ACCESS-PASSPHRASE": PASSPHRASE,
        "Content-Type": "application/json"
    }

    url = BASE_URL + path
    response = requests.get(url, headers=headers)
    print("DEBUG:", response.text)

    if response.status_code == 200:
        data = response.json()
        if data["code"] == "00000":
            usdt_balance = next((item for item in data["data"] if item["marginCoin"] == "USDT"), None)
            if usdt_balance:
                return float(usdt_balance["available"])
            else:
                return 0.0
        else:
            raise Exception(f"잔고 조회 실패: {data}")
    else:
        raise Exception(f"HTTP 오류: {response.status_code} - {response.text}")

if __name__ == "__main__":
    try:
        balance = get_futures_balance()
        print(f"현재 USDT 선물 잔고: {balance}")
    except Exception as e:
        print("[ASTRAL 오류]", e)
