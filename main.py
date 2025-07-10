import requests

TOKEN = '8121549228:AAH3Yqipscnr5rnsY0eFCDHSATC9FfU9qa0'
CHAT_ID = '7909031883'

def send_message(text):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    data = {'chat_id': CHAT_ID, 'text': text}
    requests.post(url, data=data)

if __name__ == '__main__':
    send_message("🚀 ASTRAL EXEC 자동 메시지 전송 테스트 성공!")
