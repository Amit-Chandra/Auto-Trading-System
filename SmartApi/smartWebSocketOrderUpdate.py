import ssl
import websocket
import time
import logging 
from logzero import logger
import logzero
import os

class SmartWebSocketOrderUpdate(object):
    WEBSOCKET_URI = "wss://tns.angelone.in/smart-order-update"
    HEARTBEAT_MESSAGE = "ping"  # Heartbeat message to maintain Socket connection.
    HEARTBEAT_INTERVAL_SECONDS = 10  # Interval for sending heartbeat messages to keep the connection alive.
    MAX_CONNECTION_RETRY_ATTEMPTS = 2  # Max retry attempts to establish Socket connection in case of failure.
    RETRY_DELAY_SECONDS = 10  # Delay between retry attempts when reconnecting to Socket in case of failure.
    wsapp = None  #Socket connection instance
    last_pong_timestamp = None #Timestamp of the last received pong message
    current_retry_attempt = 0  #Current retry attempt count

    def __init__(self, auth_token, api_key, client_code, feed_token):
        self.auth_token = auth_token
        self.api_key = api_key
        self.client_code = client_code
        self.feed_token = feed_token
        # Create a log folder based on the current date
        log_folder = time.strftime("%Y-%m-%d", time.localtime())
        log_folder_path = os.path.join("logs", log_folder)  # Construct the full path to the log folder
        os.makedirs(log_folder_path, exist_ok=True) # Create the log folder if it doesn't exist
        log_path = os.path.join(log_folder_path, "app.log") # Construct the full path to the log file
        logzero.logfile(log_path, loglevel=logging.INFO)  # Output logs to a date-wise log file

    def on_message(self, wsapp, message):
        logger.info("Received message: %s", message)

    def on_data(self, wsapp, message, data_type, continue_flag):
        self.on_message(wsapp, message)

    def on_open(self, wsapp):
        logger.info("Connection opened")

    def on_error(self, wsapp, error):
        logger.error("Error: %s", error)

    def on_close(self, wsapp, close_status_code, close_msg):
        logger.info("Connection closed")
        self.retry_connect()

    def on_ping(self, wsapp, data):
        timestamp = time.time()
        formatted_timestamp = time.strftime("%d-%m-%y %H:%M:%S", time.localtime(timestamp))
        logger.info("In on ping function ==> %s, Timestamp: %s", data, formatted_timestamp)

    def on_pong(self, wsapp, data):
        if data == self.HEARTBEAT_MESSAGE:
            timestamp = time.time()
            formatted_timestamp = time.strftime("%d-%m-%y %H:%M:%S", time.localtime(timestamp))
            logger.info("In on pong function ==> %s, Timestamp: %s", data, formatted_timestamp)
            self.last_pong_timestamp = timestamp
        else:
            self.on_data(wsapp, data, websocket.ABNF.OPCODE_BINARY, False)

    def check_connection_status(self):
        current_time = time.time()
        if self.last_pong_timestamp is not None and current_time - self.last_pong_timestamp > 2 * self.HEARTBEAT_INTERVAL_SECONDS:
            self.close_connection()

    def connect(self):
        headers = {
            "Authorization": self.auth_token,
            "x-api-key": self.api_key,
            "x-client-code": self.client_code,
            "x-feed-token": self.feed_token
        }
        try:
            self.wsapp = websocket.WebSocketApp(self.WEBSOCKET_URI, header=headers, on_open=self.on_open,
                                                on_error=self.on_error, on_close=self.on_close,
                                                on_data=self.on_data, on_ping=self.on_ping, on_pong=self.on_pong)
            self.wsapp.run_forever(sslopt={"cert_reqs": ssl.CERT_NONE}, ping_interval=self.HEARTBEAT_INTERVAL_SECONDS,
                                   ping_payload=self.HEARTBEAT_MESSAGE)
        except Exception as e:
            logger.error("Error connecting to WebSocket: %s", e)
            self.retry_connect()

    def retry_connect(self):
        if self.current_retry_attempt < self.MAX_CONNECTION_RETRY_ATTEMPTS:
            logger.info("Retrying connection (Attempt %s)...", self.current_retry_attempt + 1)
            time.sleep(self.RETRY_DELAY_SECONDS)
            self.current_retry_attempt += 1
            self.connect()
        else:
            logger.warning("Max retry attempts reached.")

    def close_connection(self):
        if self.wsapp:
            self.wsapp.close()
