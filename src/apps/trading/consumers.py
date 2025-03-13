'''
Used to define WebSocket consumers
Websocket consumer handles WebSocket connections
'''

# apps/trading/consumers.py
import json
from channels.generic.websocket import AsyncWebsocketConsumer

class TradeConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_group_name = 'trading_room'
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
    #Sends a message to the trading group with extracted data
    #Extracts action, card_id and user_id from the data
    async def receive(self, text_data):
        data = json.loads(text_data)
        action = data['action'] # 'offer', 'accept', 'reject', 'create_room', 'join_room'
        card_id = data['card_id']
        user_id = self.scope['user'].id
        room_name = data.get('room_name')

        if action == 'create_room':
            self.room_group_name = f'trading_room_{room_name}'
            await self.channel_layer.group_add(
                self.room_group_name,
                self.channel_name
            )
            await self.send(text_data=json.dumps({
                'message': f'Room {room_name} created',
                'room_name': room_name,
            }))
        elif action == 'join_room':
            self.room_group_name = f'trading_room_{room_name}'
            await self.channel_layer.group_add(
                self.room_group_name,
                self.channel_name
            )
            await self.send(text_data=json.dumps({
                'message': f'Joined room {room_name}',
                'room_name': room_name,
            }))
        else:
            await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'trade_offer',
                'user_id': user_id,
                'card_id': card_id,
                'action': action,
            }
        )
    #Sends the trade offer to the trading room
    async def trade_offer(self, event):
        await self.send(text_data=json.dumps({
            'user_id': event['user_id'],
            'card_id': event['card_id'],
            'action': event['action'],
        }))