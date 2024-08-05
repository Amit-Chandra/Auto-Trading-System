# package import statement
from SmartApi import SmartConnect #or from smartapi.smartConnect import SmartConnect

#import smartapi.smartExceptions(for smartExceptions)

#create object of call
obj=SmartConnect(api_key="your api key")

#login api call

data = obj.generateSession("Your Client ID","Your Password","Your totp")

refreshToken= data['data']['refreshToken']

#fetch the feedtoken
feedToken=obj.getfeedToken()

#fetch User Profile
userProfile= obj.getProfile(refreshToken)
#place order
try:
    orderparams = {
        "variety": "NORMAL",
        "tradingsymbol": "SBIN-EQ",
        "symboltoken": "3045",
        "transactiontype": "BUY",
        "exchange": "NSE",
        "ordertype": "LIMIT",
        "producttype": "INTRADAY",
        "duration": "DAY",
        "price": "19500",
        "squareoff": "0",
        "stoploss": "0",
        "quantity": "1"
        }
    orderId=obj.placeOrder(orderparams)
    print("The order id is: {}".format(orderId))
except Exception as e:
    print("Order placement failed: {}".format(e.message))
#gtt rule creation
try:
    gttCreateParams={
            "tradingsymbol" : "SBIN-EQ",
            "symboltoken" : "3045",
            "exchange" : "NSE", 
            "producttype" : "MARGIN",
            "transactiontype" : "BUY",
            "price" : 100000,
            "qty" : 10,
            "disclosedqty": 10,
            "triggerprice" : 200000,
            "timeperiod" : 365
        }
    rule_id=obj.gttCreateRule(gttCreateParams)
    print("The GTT rule id is: {}".format(rule_id))
except Exception as e:
    print("GTT Rule creation failed: {}".format(e.message))
    
#gtt rule list
try:
    status=["FORALL"] #should be a list
    page=1
    count=10
    lists=obj.gttLists(status,page,count)
except Exception as e:
    print("GTT Rule List failed: {}".format(e.message))

#Historic api
try:
    historicParam={
    "exchange": "NSE",
    "symboltoken": "3045",
    "interval": "ONE_MINUTE",
    "fromdate": "2021-02-08 09:00", 
    "todate": "2021-02-08 09:16"
    }
    obj.getCandleData(historicParam)
except Exception as e:
    print("Historic Api failed: {}".format(e.message))
#logout
try:
    logout=obj.terminateSession('Your Client Id')
    print("Logout Successfull")
except Exception as e:
    print("Logout failed: {}".format(e.message))

##Estimate Charges
# params = {
#     "orders": [
#         {
#             "product_type": "DELIVERY",
#             "transaction_type": "BUY",
#             "quantity": "10",
#             "price": "800",
#             "exchange": "NSE",
#             "symbol_name": "745AS33",
#             "token": "17117"
#         },
#         # {
#         #     "product_type": "DELIVERY",
#         #     "transaction_type": "BUY",
#         #     "quantity": "10",
#         #     "price": "800",
#         #     "exchange": "BSE",
#         #     "symbol_name": "PIICL151223",
#         #     "token": "726131"
#         # }
#     ]
# }
# estimateCharges = obj.estimateCharges(params)
# print(estimateCharges);

# params = {
#     "isin":"INE528G01035",
#     "quantity":"1"
# }
# verifyDis = obj.verifyDis(params)
# print(verifyDis);

# params = {
#     "dpId":"33200",
#     "ReqId":"2351614738654050",
#     "boid":"1203320018563571",
#     "pan":"JZTPS2255C"
# }
# generateTPIN = obj.generateTPIN(params)
# print(generateTPIN);

# params = {
#     "ReqId":"2351614738654050"
# }
# getTranStatus = obj.getTranStatus(params)
# print(getTranStatus);

# params = {
#     "name":"TCS",
#     "expirydate":"25JAN2024"
# }
# optionGreek = obj.optionGreek(params)
# print(optionGreek);

# params = {
#     "datatype":"PercOIGainers",
#     "expirytype":"NEAR" 
# }
# gainersLosers = obj.gainersLosers(params)
# print(gainersLosers);

# putCallRatio = obj.putCallRatio()
# print(putCallRatio);

# params = {
#     "expirytype":"NEAR",
#     "datatype":"Long Built Up"
# }
# OIBuildup = obj.oIBuildup(params)
# print(OIBuildup);

## WebSocket

from SmartApi.webSocket import WebSocket

FEED_TOKEN= "your feed token"
CLIENT_CODE="your client Id"
token="channel you want the information of" #"nse_cm|2885&nse_cm|1594&nse_cm|11536"
task="task" #"mw"|"sfi"|"dp"
ss = WebSocket(FEED_TOKEN, CLIENT_CODE)

def on_tick(ws, tick):
    print("Ticks: {}".format(tick))

def on_connect(ws, response):
    ws.websocket_connection() # Websocket connection  
    ws.send_request(token,task) 
    
def on_close(ws, code, reason):
    ws.stop()

# Assign the callbacks.
ss.on_ticks = on_tick
ss.on_connect = on_connect
ss.on_close = on_close

ss.connect()


