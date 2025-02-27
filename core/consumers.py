import json
import redis.asyncio as redis
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from django.conf import settings

class CodeConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["project"]
        self.room_group_name = f"code_{self.room_name}"

        try:
            self.redis = await redis.from_url(settings.REDIS_URL, decode_responses=True)
            self.user = self.scope["user"]
            
            last_code = await self.redis.get(f"project_code_{self.room_name}")

            await self.channel_layer.group_add(self.room_group_name, self.channel_name)
            await self.accept()
            if last_code:
                await self.send_json({"message": last_code})

        except Exception as error:
            print(f"Error connecting WebSocket: {error}")
            await self.close()

    async def disconnect(self, close_code):
        try:
            await self.channel_layer.group_discard(
                self.room_group_name, self.channel_name
            )
            await self.redis.aclose()

        except Exception as error:
            print(f"Error disconnecting WebSocket: {error}")

    async def receive_json(self, content):
        message = content.get("message", "").strip()

        if message:
            await self.redis.set(f"project_code_{self.room_name}", message)
            await self.channel_layer.group_send(
                self.room_group_name, {"type": "code_message", "message": message}
            )

    async def code_message(self, event):
        await self.send_json({"message": event["message"]})
