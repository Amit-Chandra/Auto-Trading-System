from logzero import logger
from SmartApi.smartConnect import SmartConnect
import pyotp

api_key = 'Your Api Key'
username = 'Your client code'
pwd = 'Your pin'
smartApi = SmartConnect(api_key)

try:
    token = "Your QR value"
    totp = pyotp.TOTP(token).now()
except Exception as e:
    logger.error("Invalid Token: The provided token is not valid.")
    raise e

correlation_id = "abcde"
data = smartApi.generateSession(username, pwd, totp)
if data['status'] == False:
    logger.error(data)
else:
    # logger.info(f"data: {data}")
    authToken = data['data']['jwtToken']
    refreshToken = data['data']['refreshToken']
    feedToken = smartApi.getfeedToken()
    # logger.info(f"Feed-Token :{feedToken}")
    res = smartApi.getProfile(refreshToken)
    # logger.info(f"Get Profile: {res}")
    smartApi.generateToken(refreshToken)
    res=res['data']['exchanges']

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
    # Method 1: Place an order and return the order ID
    orderid = smartApi.placeOrder(orderparams)
    logger.info(f"PlaceOrder : {orderid}")
    # Method 2: Place an order and return the full response
    response = smartApi.placeOrderFullResponse(orderparams)
    logger.info(f"PlaceOrder : {response}")

    modifyparams = {
        "variety": "NORMAL",
        "orderid": orderid,
        "ordertype": "LIMIT",
        "producttype": "INTRADAY",
        "duration": "DAY",
        "price": "19500",
        "quantity": "1",
        "tradingsymbol": "SBIN-EQ",
        "symboltoken": "3045",
        "exchange": "NSE"
    }
    smartApi.modifyOrder(modifyparams)
    logger.info(f"Modify Orders : {modifyparams}")

    smartApi.cancelOrder(orderid, "NORMAL")

    orderbook=smartApi.orderBook()
    logger.info(f"Order Book: {orderbook}")

    tradebook=smartApi.tradeBook()
    logger.info(f"Trade Book : {tradebook}")

    rmslimit=smartApi.rmsLimit()
    logger.info(f"RMS Limit : {rmslimit}")

    pos=smartApi.position()
    logger.info(f"Position : {pos}")

    holdings=smartApi.holding()
    logger.info(f"Holdings : {holdings}")

    allholdings=smartApi.allholding()
    logger.info(f"AllHoldings : {allholdings}")

    exchange = "NSE"
    tradingsymbol = "SBIN-EQ"
    symboltoken = 3045
    ltp=smartApi.ltpData("NSE", "SBIN-EQ", "3045")
    logger.info(f"Ltp Data : {ltp}")

    mode="FULL"
    exchangeTokens= {
    "NSE": [
    "3045"
    ]
    }
    marketData=smartApi.getMarketData(mode, exchangeTokens)
    logger.info(f"Market Data : {marketData}")

    exchange = "BSE"
    searchscrip = "Titan"
    searchScripData = smartApi.searchScrip(exchange, searchscrip)
    logger.info(f"Search Scrip Data : {searchScripData}")

    params = {
        "exchange": "NSE",
        "oldproducttype": "DELIVERY",
        "newproducttype": "MARGIN",
        "tradingsymbol": "SBIN-EQ",
        "transactiontype": "BUY",
        "quantity": 1,
        "type": "DAY"

    }

    convertposition=smartApi.convertPosition(params)

    gttCreateParams = {
        "tradingsymbol": "SBIN-EQ",
        "symboltoken": "3045",
        "exchange": "NSE",
        "producttype": "MARGIN",
        "transactiontype": "BUY",
        "price": 100000,
        "qty": 10,
        "disclosedqty": 10,
        "triggerprice": 200000,
        "timeperiod": 365
    }
    rule_id = smartApi.gttCreateRule(gttCreateParams)
    logger.info(f"Gtt Rule: {rule_id}")

    gttModifyParams = {
        "id": rule_id,
        "symboltoken": "3045",
        "exchange": "NSE",
        "price": 19500,
        "quantity": 10,
        "triggerprice": 200000,
        "disclosedqty": 10,
        "timeperiod": 365
    }
    modified_id = smartApi.gttModifyRule(gttModifyParams)
    logger.info(f"Gtt Modified Rule: {modified_id}")

    cancelParams = {
        "id": rule_id,
        "symboltoken": "3045",
        "exchange": "NSE"
    }

    cancelled_id = smartApi.gttCancelRule(cancelParams)
    logger.info(f"gtt Cancel Rule: {cancelled_id}")

    gttdetails=smartApi.gttDetails(rule_id)
    logger.info(f"GTT Details: {gttdetails}")

    smartApi.gttLists('List of status', '<page>', '<count>')

    candleParams={
        "exchange": "NSE",
        "symboltoken": "3045",
        "interval": "ONE_MINUTE",
        "fromdate": "2021-02-10 09:15",
        "todate": "2021-02-10 09:16"
    }
    candledetails=smartApi.getCandleData(candleParams)
    logger.info(f"Historical Data: {candledetails}")

    qParam ="your uniqueorderid"
    data = smartApi.individual_order_details(qParam)
    logger.info(f"Individual_order_details: {data}")

    params = {
        "positions": [{
        "exchange": "NSE",
        "qty": 50,
        "price": 0,
        "productType": "DELIVERY",
        "token": "12740",
        "tradeType": "BUY"
        }]
    }
    margin_api_result=smartApi.getMarginApi(params)
    logger.info(f"margin_api_result: {margin_api_result}")

    terminate=smartApi.terminateSession('Your client code')
    logger.info(f"Connection Close: {terminate}")

    # # Websocket Programming

    from SmartApi.smartWebSocketV2 import SmartWebSocketV2

    AUTH_TOKEN = authToken
    API_KEY = api_key
    CLIENT_CODE = username
    FEED_TOKEN = feedToken
    # correlation_id = "abc123"
    action = 1
    mode = 1

    token_list = [
        {
            "exchangeType": 1,
            "tokens": ["26009","1594"]
        }
    ]
    token_list1 = [
        {
            "action": 0,
            "exchangeType": 1,
            "tokens": ["26009"]
        }
    ]

    #retry_strategy=0 for simple retry mechanism
    sws = SmartWebSocketV2(AUTH_TOKEN, API_KEY, CLIENT_CODE, FEED_TOKEN,max_retry_attempt=2, retry_strategy=0, retry_delay=10, retry_duration=30)

    #retry_strategy=1 for exponential retry mechanism
    # sws = SmartWebSocketV2(AUTH_TOKEN, API_KEY, CLIENT_CODE, FEED_TOKEN,max_retry_attempt=3, retry_strategy=1, retry_delay=10,retry_multiplier=2, retry_duration=30)

    def on_data(wsapp, message):
        logger.info("Ticks: {}".format(message))
        close_connection()

    def on_control_message(wsapp, message):
        logger.info(f"Control Message: {message}")

    def on_open(wsapp):
        logger.info("on open")
        some_error_condition = False
        if some_error_condition:
            error_message = "Simulated error"
            if hasattr(wsapp, 'on_error'):
                wsapp.on_error("Custom Error Type", error_message)
        else:
            sws.subscribe(correlation_id, mode, token_list)
            # sws.unsubscribe(correlation_id, mode, token_list1)

    def on_error(wsapp, error):
        logger.error(error)

    def on_close(wsapp):
        logger.info("Close")

    def close_connection():
        sws.close_connection()


    # Assign the callbacks.
    sws.on_open = on_open
    sws.on_data = on_data
    sws.on_error = on_error
    sws.on_close = on_close
    sws.on_control_message = on_control_message

    sws.connect()


    ########################### SmartWebSocket OrderUpdate Sample Code Start Here ###########################
    from SmartApi.smartWebSocketOrderUpdate import SmartWebSocketOrderUpdate
    client = SmartWebSocketOrderUpdate(AUTH_TOKEN, API_KEY, CLIENT_CODE, FEED_TOKEN)
    client.connect()
    ########################### SmartWebSocket OrderUpdate Sample Code End Here ###########################
