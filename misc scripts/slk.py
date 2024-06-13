from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from dotenv import load_dotenv
import os

load_dotenv()
token = os.getenv("BOT_TOKEN")
client = WebClient(token)

def message(msg):
    msg = "Status Code From Script: " + msg
    channel_id = "C077G0V5CRZ"

    try:
        response = client.files_upload_v2(
            channel=channel_id,
            file="log.json",
            title="Log File",
            initial_comment=msg,
        )

    except SlackApiError as e:
        print(f"Error sending message: {e.response['error']}")