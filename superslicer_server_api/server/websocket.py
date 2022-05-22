from abc import ABC
from typing import List

import orjson
import redis
from tornado.websocket import WebSocketHandler

REDIS_HOST = '127.0.0.1'
REDIS_PORT = 6379
REDIS_DB = 0


def redis_connect(host, port, db):
    connection = redis.Redis(host, port, db)
    return connection


class ServerSocketHandler(WebSocketHandler, ABC):
    def initialize(self):
        self.message = None
        # self.stdout = []
        # self.subscribed = False
        # self.redis_host = REDIS_HOST
        # self.redis_port = REDIS_PORT
        # self.redis_db = REDIS_DB
        # self.redis = redis_connect(self.redis_host, self.redis_port, self.redis_db)
        # self.redis_pubsub = self.redis.pubsub()

    def check_origin(self, origin: str) -> bool:
        # To allow connections from any subdomain of your site
        # parsed_origin = urllib.parse.urlparse(origin)
        # return parsed_origin.netloc.endswith(".mydomain.com")
        return True  # Allow all origin

    def open(self, channel):
        # if not self.wsm.has_channel(channel):
        #     payload = orjson.dumps({'error': 'Slicing operation already terminated or there were no slicing operation'})
        #     self.write_message(payload)
        #     self.close(1000, 'Operation terminated.Channel:' + channel)
        #     return
        # self.redis_pubsub.subscribe(channel)
        # print(self.redis_pubsub.get_message())
        # pubsub_message = orjson.loads()
        # self.subscribed = pubsub_message['type'] == 'subscribe'
        print("Client connected to channel : " + channel)
        payload = orjson.dumps({'message': f'Connected to SuperSlicer Server on channel "{channel}"'})
        self.write_message(payload)

    def on_message(self, message):
        self.message = orjson.loads(message)
        payload = orjson.dumps({
            'received': message,
            'loaded': self.message,
            'response': 'response'
        })
        self.write_message(payload)

    def on_close(self):
        print('Close code : ' + str(self.close_code))
        print(self.close_reason)
        if self.close_reason:
            close_reason = self.close_reason.split('.')
            channel = close_reason[1].split(':')[1]
            print("Server close connection to channel : " + channel)
            return
        print("Client disconnected")

    # def add_channel(self, channel):
    #     self.channels.append(channel)
    #
    # def remove_channel(self, channel):
    #     if channel in self.channels:
    #         self.channels.remove(channel)
    #
    def publish_message(self, channel, message):
        payload = orjson.dumps({
            'message': message
        })
        print("Message received from process : " + channel)
        # self.redis.publish(channel, payload)
        self.write_message(payload)
