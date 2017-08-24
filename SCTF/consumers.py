from channels.auth import channel_session_user, http_session_user
from django.http import HttpResponse
from channels.handler import AsgiHandler

# In consumers.py
from channels import Group

# Connected to websocket.connect
@http_session_user
def ws_add(message):
    # Accept the connection
    message.reply_channel.send({"accept": True})
    # Add to the chat group
    print(message.user)
    Group("chat").add(message.reply_channel)

# Connected to websocket.receive
def ws_message(message):
    Group("chat").send({
        "text": "[user] %s" % message.content['text'],
    })

# Connected to websocket.disconnect
def ws_disconnect(message):
    Group("chat").discard(message.reply_channel)


def send_message(text):
    Group("chat").send({"text": text})