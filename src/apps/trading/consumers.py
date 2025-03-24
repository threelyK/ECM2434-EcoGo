'''
Used to define WebSocket consumers
Websocket consumer handles WebSocket connections
'''

# apps/trading/consumers.py
import json
from channels.generic.websocket import WebsocketConsumer

from .TradingRoom import TradingRoom, get_room, get_response_func, rooms

class TradeConsumer(WebsocketConsumer):
    def connect(self):
        self.room = None
        self.user = self.scope["user"]
        self.accept()

    def receive(self, text_data=None, bytes_data=None):
        data = json.loads(text_data)

        #State flag for inital joining of a room
        if data["state_flag"] == "J":
            self.room_name = data["room_name"]
            (room, response_owner) = get_room(rooms, self.room_name)
            self.room = room
            response_func = get_response_func(room.room_owner, response_owner, self.user, self.send)
            room.join_room(self.user, response_func)
        #State flag for inital starting of a room
        elif data["state_flag"] == "S":
            self.room_name = data["room_name"]
            room = TradingRoom(self.user)
            rooms.append((self.room_name, room, self.send))
            self.room = room
            print(rooms)

        else:
            self.room.handle(data, self.user)

    def disconnect(self, code):
        print("socket disconnected")
        if (not self.room is None) and not code == 1000 and not self.room.state == "W": #Room exists and code is non-standard
            self.room.disconnect(self.user)

        if not self.room is None:
            if self.room.room_owner == self.user: #Only remove the room if you are user
                (room, func) = get_room(rooms, self.room_name)
                rooms.remove((self.room_name, room, func))


        