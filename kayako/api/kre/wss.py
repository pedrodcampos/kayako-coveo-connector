import websocket
from websocket._exceptions import WebSocketConnectionClosedException
import threading
import json
import logging
import time
from kayako.api.kre.errors import KayakoKreError

from kayako.api.kre.helpers import (KrePingPayload,
                                KreSubscriptionPayload,
                                get_new_ref,
                                make_wss_url,
                                PING_TOPIC, MESSAGE_REF,
                                REPLY_EVENT)


class KayakoKre():

    def __init__(self, requests, ping_interval=3, retry_interval=30, auto_reconnect=True, on_open=None):
        self.__ping_thread = None
        self.retry_interval = retry_interval
        self.__requests = requests
        self.__callbacks = {}
        self.__success_callbacks = {}
        self.__subscriptions = set()
        self.__ws = None
        self.__last_pong = None
        self.__last_ping = None
        self.__auto_reconnect = auto_reconnect
        self.__is_connected = False
        self.__custom_on_open = on_open

        self.ping_interval = ping_interval

    @property
    def is_connected(self):
        return self.__is_connected

    def __get_websocket_url(self):
        session = self.__requests.user_session
        return make_wss_url(session)

    def subscribe(self, channel, callback, on_success=None):
        self.__subscriptions.update([channel])
        self.__callbacks.update({channel: callback})
        if on_success:
            self.__success_callbacks.update({channel: on_success})
        payload = KreSubscriptionPayload(
            channel, get_new_ref()).to_json()
        try:
            self.__ws.send(payload)
        except WebSocketConnectionClosedException:
            logging.critical(
                'Connection was closed before finishing subscription')

    def __handle_reply(self, data):
        topic = data['topic']
        if topic in self.__success_callbacks:
            payload = data['payload']
            status = payload['status']
            if status == 'ok':
                thread = threading.Thread(
                    name='kre-callback', target=self.__success_callbacks[topic], args=(data,))
                thread.setDaemon = True
                thread.start()
                self.__success_callbacks.pop(topic)

    def __is_reply(self, data):
        return data['event'] == REPLY_EVENT

    def __is_pong(self, data, ws):
        if self.__is_reply(data):
            return data['topic'] == PING_TOPIC
        return False

    def __ping(self):
        def send_ping(interval):
            while self.is_connected:
                ref = get_new_ref()
                payload = KrePingPayload(ref).to_json()
                self.__last_ping = ref
                try:
                    self.__ws.send(payload)
                    logging.debug("ping sent: {}".format(ref))
                except Exception as e:
                    logging.error(e)

                time.sleep(self.ping_interval)
                if self.is_connected:
                    if self.__last_pong != self.__last_ping:
                        logging.critical('Last pong was not received.')
                        self.__ws.close()
                        break
                else:
                    logging.warning(
                        'Connection was closed before last pong was received.')
                    break

        thread = threading.Thread(name='kre-ping',
                                  target=send_ping,
                                  args=(self.ping_interval,))
        self.__ping_thread = thread
        thread.setDaemon(True)
        thread.start()

    def __on_open(self, ws):
        logging.info('Connected')
        self.__is_connected = True
        self.__ping()
        if self.__custom_on_open:
            self.__custom_on_open()

    def __on_message(self, ws, message):
        logging.debug('Incoming message:')
        logging.debug(message)

        data = json.loads(message)
        if self.__is_pong(data, ws):
            self.__last_pong = int(data[MESSAGE_REF])
            logging.debug(f"pong received: {data[MESSAGE_REF]}")
        if self.__is_reply(data):
            self.__handle_reply(data)
        else:
            topic = data['topic']
            if topic in self.__callbacks:
                self.__callbacks[topic](data['event'], data)

    def __on_error(self, ws, error):
        logging.error(error)

    def __on_close(self, *args):
        pass

    def stop(self):
        if self.__is_connected:
            self.__ws.close()

    def listen(self, auto_reconnect=True,
               enable_trace=False):
        def hook_on_message(*args):
            self.__on_message(*args)

        def hook_on_error(*args):
            self.__on_error(*args)

        def hook_on_close(*args):
            self.__on_close(*args)

        def hook_on_open(*args):
            self.__on_open(*args)

        def start(ws):
            while True:
                logging.info('Connecting')
                session = self.__requests.user_session
                wss_url = make_wss_url(session)
                ws.url = wss_url
                ws.run_forever()
                logging.info('Connection Closed')

                self.__is_connected = False
                if self.__ping_thread:
                    if self.__ping_thread.is_alive():
                        self.__ping_thread.join()
                if not self.__auto_reconnect:
                    break
                logging.info(
                    f'Auto-reconnect starts in {self.retry_interval} seconds')
                time.sleep(self.retry_interval)

        self.__auto_reconnect = auto_reconnect
        websocket.enableTrace(enable_trace)
        wss_url = self.__get_websocket_url()
        ws = websocket.WebSocketApp(wss_url)
        self.__ws = ws
        ws.on_message = hook_on_message
        ws.on_error = hook_on_error
        ws.on_close = hook_on_close
        ws.on_open = hook_on_open
        self.__listening_thread = threading.Thread(name='kre-listening-thread',
                                                   target=start, args=(ws,))
        self.__listening_thread.setDaemon = True
        self.__listening_thread.start()
