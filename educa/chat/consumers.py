import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import async_to_sync
from django.utils import timezone


class ChatConsumer(AsyncWebsocketConsumer):
    """Потребитель."""

    async def connect(self):
        """Устанавливает соединение."""
        self.user = self.scope['user']
        self.id = self.scope['url_route']['kwargs']['course_id']
        self.room_group_name = f'chat_{self.id}'
        # Присоединиться к группе чат-комнаты
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        # Принять соединение
        await self.accept()

    async def disconnect(self, close_code):
        """Разрывает соединение."""
        # Покинуть группу чат-комнаты
        await self.channel_layer.group.discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        """Получает сообщение из web-socket."""
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        # Отправить сообщение в группу чат-комнаты.
        self.channel_layer.group_send(self.room_group_name,
                                      {
                                          'type': 'chat_message',
                                          'message': message,
                                          'user': self.user.username,
                                          'datetime': timezone.now().isoformat(),
                                      }
                                      )

    async def chat_message(self, event):
        """Получает сообщение из группы чат-комнаты."""
        # Отправляет сообщение в web-socket
        await self.send(text_data=json.dumps(event))
