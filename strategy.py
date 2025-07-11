from utils import send_telegram_message

def should_exit_position(rsi):
    if rsi > 70:
        send_telegram_message(f"📈 RSI: {rsi} - 익절 조건 만족. 포지션 종료 권고")
        return True
    return False
