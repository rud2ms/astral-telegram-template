from utils import send_telegram_message

def enter_trade(symbol, side):
    send_telegram_message(f"💸 실거래 진입: {symbol} - {side.upper()}")
