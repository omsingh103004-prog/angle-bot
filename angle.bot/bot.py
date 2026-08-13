from SmartApi import SmartConnect
import pyotp
import time

API_KEY = "nxBQe7AG"
CLIENT_CODE = "O61849531"
MPIN = "2004"
TOTP_SECRET = "U5KLWHH6OV37BZLVSFAIGLT7HY"

def auto_login():
    api = SmartConnect(api_key=API_KEY)
    totp = pyotp.TOTP(TOTP_SECRET).now()
    data = api.generateSession(CLIENT_CODE, MPIN, totp)

    if data["status"]:
        print("Angel One Auto Login Successful ✅")
        return api
    else:
        print("Login Failed ❌")
        return None

api = auto_login()

while True:
    try:
        # NIFTY
        nifty = api.ltpData("NSE", "NIFTY", "26000")
        nifty_price = nifty["data"]["ltp"]

        # SENSEX
        sensex = api.ltpData("BSE", "SENSEX", "99919000")
        sensex_price = sensex["data"]["ltp"]

        print(f"📈 NIFTY  : {nifty_price}")
        print(f"📈 SENSEX : {sensex_price}")
        print("----------------------")

    except Exception as e:
        print("Error:", e)

    time.sleep(5)