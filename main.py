import os
import time
import hmac
import hashlib
import requests

# 환경변수에서 키 불러오기
API_KEY = os.environ['API_KEY']
SECRET_KEY = os.environ['SECRET_KEY']
PASSPHRASE = os.environ['PASSPHRASE']

# 서명 생성 함수
def generate_signature(timestamp, method, request_path, body):
    message = f'{timestamp}{method}{request_path}{body}'
    signature = hmac.new(
        bytes(SECRET_KEY, encoding='utf-8'),
        msg=bytes(message, encoding='utf-8'),
        digestmod=hashlib.sha256
    ).hexdigest()
    return signature

# 잔고 조회 요청
def get_balance():
    method = "GET"
    request_path = "/api/mix/v1/account/USDT_balance"
    body = ""
    timestamp = str(int(time.time() * 1000))
    signature = generate_signature(timestamp, method, request_path, body)

    headers = {
        "ACCESS-KEY": API_KEY,
        "ACCESS-SIGN": signature,
        "ACCESS-TIMESTAMP": timestamp,
        "ACCESS-PASSPHRASE": PASSPHRASE,
        "Content-Type": "application/json"
    }

    url = "https://api.bitget.com" + request_path
    response = requests.get(url, headers=headers)
    print("DEBUG:", response.text)
    return response.json()

# 테스트 실행
if __name__ == "__main__":
    result = get_balance()
    print(result)
