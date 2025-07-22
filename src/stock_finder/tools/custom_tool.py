import os 
import requests
from crewai.tools import BaseTool
from typing import Type
from pydantic import BaseModel, Field


class PushoverNotification(BaseModel):
    """A message to be sent to the user via Pushover url on the Pushover app"""
    message: str = Field(..., description="The message to be sent to the user.")

class PushoverNotificationTool(BaseTool):
    name: str = "Send a Push Notification"
    description: str = (
        "This tool is used to send a push notification to the user."
    )
    args_schema: Type[BaseModel] = PushoverNotification

    def _run(self, message: str) -> str:
        pushover_user = os.getenv("PUSHOVER_USER")
        pushover_token = os.getenv("PUSHOVER_TOKEN")
        pushover_url = "https://api.pushover.net/1/messages.json"

        print(f"Push: {message}")
        payload = {"user": pushover_user, "token": pushover_token, "message": message}
        requests.post(pushover_url, data=payload)
        return '{"notification": "ok"}'
