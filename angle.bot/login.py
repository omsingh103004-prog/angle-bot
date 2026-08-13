from SmartApi import SmartConnect
import pyotp

api_key = "nxBQe7AG"
client_code = "O61849531"
mpin = "2004"
totp_secret = "U5KLWHH6OV37BZLVSFAIGLT7HY"

totp = pyotp.TOTP(totp_secret).now()

api = SmartConnect(api_key=api_key)

data = api.generateSession(client_code, mpin, totp)

print(data)