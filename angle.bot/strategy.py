from SmartApi import SmartConnect
import pyotp
import time
from datetime import datetime

# ================== ANGEL ONE DETAILS ==================
API_KEY = "nxBQe7AG"
CLIENT_CODE = "O61849531"
MPIN = "2004"
TOTP_SECRET = "U5KLWHH6OV37BZLVSFAIGLT7HY"


# ================== AUTO LOGIN ==================
def auto_login():
    api = SmartConnect(api_key=API_KEY)
    totp = pyotp.TOTP(TOTP_SECRET).now()

    data = api.generateSession(CLIENT_CODE, MPIN, totp)

    if data["status"]:
        print("✅ Angel One Auto Login Successful")
        return api

    print("❌ Login Failed")
    return None


api = auto_login()


# ================== MARGIN ==================
def get_available_margin():
    try:
        rms = api.rmsLimit()
        return float(rms["data"]["availablecash"])
    except:
        return 0.0


# ================== ROUNDING ==================
def round_to_step(price, step):
    return int(round(price / step) * step)


# ================== STRIKE SELECTION ==================
def get_nifty_strike(price, signal):
    atm = round_to_step(price, 50)

    if signal == "BUY CE":
        return f"NIFTY {atm + 250} CE"
    elif signal == "BUY PE":
        return f"NIFTY {atm - 250} PE"

    return "-"


def get_sensex_strike(price, signal):
    atm = round_to_step(price, 100)

    if signal == "BUY CE":
        return f"SENSEX {atm + 500} CE"
    elif signal == "BUY PE":
        return f"SENSEX {atm - 500} PE"

    return "-"


# ================== SIGNAL LOGIC ==================
def get_signal(price, ema9, ema20, vwap, rsi, resistance, support):
    if price > resistance and ema9 > ema20 and price > vwap and rsi > 55:
        return "BUY CE"

    if price < support and ema9 < ema20 and price < vwap and rsi < 45:
        return "BUY PE"

    return "WAIT"


# ================== LOT CALCULATION ==================
def calculate_lots(margin, option_price):
    if option_price <= 0:
        return 1

    qty_per_lot = 75
    max_lots = int(margin // (option_price * qty_per_lot))

    return max(1, min(max_lots, 4))


# ================== DAILY SETTINGS ==================
trades_today = 0
MAX_TRADES = 4


# ================== LIVE LOOP ==================
while True:
    margin = get_available_margin()
    daily_target = round(margin * 0.15, 2)

    current_time = datetime.now().strftime("%H:%M")

    # ---------------- NIFTY ----------------
    nifty_price = 24435.95
    nifty_support = 24435.95
    nifty_resistance = 24454.95
    nifty_ema9 = 24448.18
    nifty_ema20 = 24445.57
    nifty_rsi = 58
    nifty_vwap = 24442.82

    nifty_signal = get_signal(
        nifty_price,
        nifty_ema9,
        nifty_ema20,
        nifty_vwap,
        nifty_rsi,
        nifty_resistance,
        nifty_support,
    )

    # --------- DAILY COMPULSORY TRADE ---------
    if nifty_signal == "WAIT" and trades_today == 0 and current_time >= "09:20":
        if nifty_ema9 > nifty_ema20 and nifty_price > nifty_vwap:
            nifty_signal = "BUY CE"
        else:
            nifty_signal = "BUY PE"

    nifty_strike = get_nifty_strike(nifty_price, nifty_signal)
    nifty_lots = calculate_lots(margin, 14)

    # ---------------- SENSEX ----------------
    sensex_price = 77966.35
    sensex_support = 77966.35
    sensex_resistance = 77985.35
    sensex_ema9 = 77978.58
    sensex_ema20 = 77975.97
    sensex_rsi = 58
    sensex_vwap = 77973.22

    sensex_signal = get_signal(
        sensex_price,
        sensex_ema9,
        sensex_ema20,
        sensex_vwap,
        sensex_rsi,
        sensex_resistance,
        sensex_support,
    )

    if sensex_signal == "WAIT" and trades_today == 0 and current_time >= "09:20":
        if sensex_ema9 > sensex_ema20 and sensex_price > sensex_vwap:
            sensex_signal = "BUY CE"
        else:
            sensex_signal = "BUY PE"

    sensex_strike = get_sensex_strike(sensex_price, sensex_signal)
    sensex_lots = calculate_lots(margin, 28)

    # ================== OUTPUT ==================
    print("\n" + "=" * 60)
    print(datetime.now().strftime("%d-%m-%Y %H:%M:%S"))
    print("=" * 60)
    print(f"💰 Available Margin : ₹{margin:.2f}")
    print(f"🎯 Daily Target (15%) : ₹{daily_target:.2f}")
    print(f"📊 Trades Today : {trades_today}/{MAX_TRADES}")

    print("\n📈 NIFTY")
    print(f"Price       : {nifty_price}")
    print(f"Support     : {nifty_support}")
    print(f"Resistance  : {nifty_resistance}")
    print(f"EMA9        : {nifty_ema9}")
    print(f"EMA20       : {nifty_ema20}")
    print(f"RSI         : {nifty_rsi}")
    print(f"VWAP        : {nifty_vwap}")
    print(f"Signal      : {nifty_signal}")
    print(f"Strike      : {nifty_strike}")
    print(f"Lots        : {nifty_lots}")
    print("Target / SL : +4 / -4")

    print("\n📉 SENSEX")
    print(f"Price       : {sensex_price}")
    print(f"Support     : {sensex_support}")
    print(f"Resistance  : {sensex_resistance}")
    print(f"EMA9        : {sensex_ema9}")
    print(f"EMA20       : {sensex_ema20}")
    print(f"RSI         : {sensex_rsi}")
    print(f"VWAP        : {sensex_vwap}")
    print(f"Signal      : {sensex_signal}")
    print(f"Strike      : {sensex_strike}")
    print(f"Lots        : {sensex_lots}")
    print("Target / SL : +10 / -9")

    print("=" * 60)

    # ---------------- DAILY TARGET STOP ----------------
    if daily_target <= 0:
        print("🎯 Daily target reached. Bot stopped.")
        break

    time.sleep(30)