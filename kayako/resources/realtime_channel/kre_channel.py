from kayako.api.kre.wss import KayakoKre
from kayako.resources.core.users import KayakoUsers
from kayako.api.requests import KayakoRequests
from kayako.api.errors import KayakoAPIError
from kayako.api.kre.helpers import PRESENCE_DIFF_EVENT, PRESENCE_STATE_EVENT
from kayako.api.kre.errors import KayakoKreError
from threading import Event, Thread
from collections import OrderedDict


class KayakoKreChannel:
    def __init__(self, requests: KayakoRequests):
        self.__requests = requests
        self.__kre = KayakoKre(requests,
                               on_open=self.__on_open)
        self.__event_callback = None
        self.__agents_channel = None
        self.__success_subscribe = Event()

    def has_event_callback(self):
        return self.__event_callback is not None

    def __on_open(self):
        def subscribe():
            self.__agents_channel = self.get_agents_presence_channel()
            for channel, _ in self.__agents_channel.items():
                self.__kre.subscribe(
                    channel, self.__channel_listener,  self.__on_success_subscribe)
                if not self.__success_subscribe.wait(30):
                    self.__kre.stop()
                    raise KayakoKreError(
                        'Subscription response was not received')

        thread = Thread(name='kre-subscriptions', target=subscribe)
        thread.setDaemon = True
        thread.start()

    def get_agents_presence_channel(self):
        users = KayakoUsers(self.__requests)
        agents = users.get_by_role('agent', fields='presence_channel')
        channels = {}
        current_user_id = self.__requests.user_session.user.id
        for agent in agents:
            if agent['id'] != current_user_id:
                channels.update({agent['presence_channel']: str(agent['id'])})
        return channels

    def event_subscribe(self, on_event):
        self.__event_callback = on_event

    def __dispatch(self, event, data):
        thread = Thread(name='kre-channel-{}-handle-{}'.format(event, data['user_id']),
                        target=self.__event_callback, args=(event, data,))
        thread.setDaemon = True
        thread.start()

    def __get_user_sessions(self, payload):
        user_sessions = {}
        for key, value in payload.items():
            user_sessions.update({key: []})
            metas = value['metas']
            for session in metas:
                user_sessions[key].append(session['phx_ref'])
        return user_sessions

    def __is_presence_state_event(self, message):
        return message['event'] == PRESENCE_STATE_EVENT

    def __is_presence_diff_event(self, message):
        return message['event'] == PRESENCE_DIFF_EVENT

    def __handle_event(self, event, message):
        def get_user_data(topic,  payload):
            user_sessions = self.__get_user_sessions(payload)
            if len(user_sessions) > 0:
                topic = message['topic']
                user_id = self.__agents_channel[topic]
                if user_id in user_sessions:
                    data = {'user_id': user_id,
                            'sessions': user_sessions[user_id]}
                    return data
            return {}

        def handle_presence_state(message):
            payload = message['payload']
            topic = message['topic']
            user_data = get_user_data(topic, payload)
            if len(user_data) > 0:
                self.__dispatch('presence_state', user_data)

        def handle_presence_diff_joins(message):
            payload = message['payload']['joins']
            topic = message['topic']
            user_data = get_user_data(topic, payload)
            if len(user_data) > 0:
                self.__dispatch('join', user_data)

        def handle_presence_diff_leaves(message):
            payload = message['payload']['leaves']
            topic = message['topic']
            user_data = get_user_data(topic, payload)
            if len(user_data) > 0:
                self.__dispatch('leave', user_data)

        if self.has_event_callback():
            if event == PRESENCE_STATE_EVENT:
                handle_presence_state(message)
            elif event == PRESENCE_DIFF_EVENT:
                handle_presence_diff_joins(message)
                handle_presence_diff_leaves(message)

    def __on_success_subscribe(self, data):
        self.__success_subscribe.set()

    def __channel_listener(self, event, message):
        self.__handle_event(event, message)

    def listen(self, auto_reconnect=True, enable_trace=False):
        self.__kre.listen(auto_reconnect, enable_trace)
