from signals import get_rsi
from trade import enter_trade
from strategy import should_exit_position
from utils import get_balance, send_telegram_message

def run_astral_loop():
    send_telegram_message("🚀 ASTRAL EXEC 전략 루프 시작됨")

    balance = get_balance()
    if balance <= 0:
        send_telegram_message("⚠️ 잔고 부족 또는 조회 실패")
        send_telegram_message("✅ 전략 루프 종료됨")
        return

    rsi = get_rsi("BTCUSDT", "15m", 14)
    if rsi is None:
        send_telegram_message("⚠️ RSI 계산 실패. 전략 중단")
        send_telegram_message("✅ 전략 루프 종료됨")
        return

    if rsi < 30:
        send_telegram_message(f"📉 RSI: {rsi} - 매수 조건 만족")
        enter_trade("BTCUSDT", "open_long")
    elif should_exit_position(rsi):
        send_telegram_message("🚪 포지션 청산 조건 만족 - 전략 루프 종료")
    else:
        send_telegram_message(f"📊 RSI: {rsi} - 조건 불만족, 대기")

    send_telegram_message("✅ 전략 루프 종료됨")
