import time
import hmac
import hashlib
import requests
import json

API_KEY = "bg_80625110d7152ca34ef7b5a63d0a1e9c"
SECRET_KEY = "47c8862d0c869f978d06deaa95f08ca4aff54c74f9a71bd84a53d27412a2ed14"
PASSPHRASE = "sodlfmaruddms1"

def get_timestamp():
    return str(int(time.time() * 1000))

def sign_request(timestamp, method, request_path, body=None):
    if body:
        message = f"{timestamp}{method.upper()}{request_path}{body}"
    else:
        message = f"{timestamp}{method.upper()}{request_path}"

    signature = hmac.new(
        SECRET_KEY.encode("utf-8"),
        message.encode("utf-8"),
        hashlib.sha256
    ).hexdigest()

    return signature

def get_usdt_balance():
    timestamp = get_timestamp()
    method = "GET"
    request_path = "/api/mix/v1/account/accounts?productType=USDT-FUTURES"
    url = "https://api.bitget.com" + request_path

    sign = sign_request(timestamp, method, request_path)

    headers = {
        "ACCESS-KEY": API_KEY,
        "ACCESS-SIGN": sign,
        "ACCESS-TIMESTAMP": timestamp,
        "ACCESS-PASSPHRASE": PASSPHRASE,
        "Content-Type": "application/json"
    }

    response = requests.get(url, headers=headers)
    print("DEBUG:", response.text)

    if response.status_code == 200 and response.json().get("code") == "00000":
        margin = float(response.json()["data"][0]["marginBalance"])
        return margin
    else:
        print("❌ 오류 발생:", response.text)
        return 0

# 실행
balance = get_usdt_balance()
print("현재 잔고:", balance)
