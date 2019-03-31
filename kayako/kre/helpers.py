import json
import random
import urllib

WEBSOCKET_URL = 'wss://kre.kayako.net/socket/websocket'
VSN = '1.0.0'

JOIN_EVENT = 'phx_join'
PING_EVENT = 'heartbeat'
DEFAULT_DEVICE = 'kayako_bot'
PING_TOPIC = 'phoenix'
MESSAGE_REF = 'ref'
REPLY_EVENT = 'phx_reply'
PRESENCE_STATE_EVENT = 'presence_state'
PRESENCE_DIFF_EVENT = 'presence_diff'
CHANGE_EVENT = 'CHANGE'
DEVICE_KEY = 'device_id'
REF_LENGHT = 6


def get_new_ref():
    return random.randint(0, 10**REF_LENGHT-1)


def make_wss_url(session):
    params = {'instance': session.instance_name,
              'session_id': session.id,
              'user_agent': session.user_agent,
              'vsn': VSN}
    query = urllib.parse.urlencode(params)
    url = '?'.join([WEBSOCKET_URL, query])
    return url


class KrePayload():

    def to_json(self):
        return json.dumps(self.__dict__)


class KreSubscriptionPayload(KrePayload):
    def __init__(self, channel, ref):
        self.topic = channel
        self.event = JOIN_EVENT
        self.payload = {}
        self.ref = ref


class KrePingPayload(KrePayload):
    def __init__(self, ref):
        self.topic = PING_TOPIC
        self.event = PING_EVENT
        self.payload = {}
        self.ref = str(ref)
