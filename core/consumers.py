import json
from channels.generic.websocket import AsyncJsonWebsocketConsumer

class CodeConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["project"]
        self.room_group_name = f"code_{self.room_name}"

        try:
            await self.channel_layer.group_add(self.room_group_name, self.channel_name)
            await self.accept()

        except Exception as error:
            print(f"Error connecting WebSocket: {error}")
            await self.close()

    async def disconnect(self, close_code):
        try:
            await self.channel_layer.group_discard(
                self.room_group_name, self.channel_name
            )
        except Exception as error:
            print(f"Error disconnecting WebSocket: {error}")

    async def receive_json(self, content):
        message = content.get("message", "").strip()

        if message:
            await self.channel_layer.group_send(
                self.room_group_name, {"type": "code_message", "message": message}
            )

    async def code_message(self, event):
        await self.send_json({"message": event["message"]})
