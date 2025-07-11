import requests

def get_rsi(symbol, interval, period):
    try:
        url = f"https://api.bitget.com/api/mix/v1/market/candles?symbol={symbol}_UMCBL&granularity={interval}&limit={period + 1}"
        response = requests.get(url)
        closes = [float(kline[4]) for kline in response.json()["data"]]

        if len(closes) < period + 1:
            return None

        gains = []
        losses = []
        for i in range(1, len(closes)):
            delta = closes[i] - closes[i - 1]
            if delta >= 0:
                gains.append(delta)
                losses.append(0)
            else:
                gains.append(0)
                losses.append(abs(delta))

        avg_gain = sum(gains[-period:]) / period
        avg_loss = sum(losses[-period:]) / period

        if avg_loss == 0:
            return 100

        rs = avg_gain / avg_loss
        return round(100 - (100 / (1 + rs)), 2)
    except Exception:
        return None
