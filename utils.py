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

def generate_signature(timestamp, method, path, query_string, body=""):
    message = f"{timestamp}{method}{path}{query_string}{body}"
    mac = hmac.new(API_SECRET.encode(), message.encode(), digestmod="sha256")
    return base64.b64encode(mac.digest()).decode()

def get_balance():
    try:
        timestamp = str(int(time.time() * 1000))
        method = "GET"
        path = "/api/mix/v1/account/accounts"
        query_string = "?productType=USDT_PERPETUAL"
        request_path = path + query_string
        url = "https://api.bitget.com" + request_path

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
            data = response.json()
            return float(data['data'][0]['available'])
        else:
            return 0.0
    except Exception as e:
        print("잔고 조회 오류:", e)
        return 0.0

def send_telegram_message(message):
    try:
        url = f"https://api.telegram.org/bot{TG_TOKEN}/sendMessage"
        data = {"chat_id": TG_USER_ID, "text": message}
        requests.post(url, json=data)
    except:
        print("텔레그램 메시지 전송 실패")
