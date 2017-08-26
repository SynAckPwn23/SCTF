import json

from channels.auth import http_session_user

# In consumers.py
from channels import Group

# Connected to websocket.connect
@http_session_user
def ws_add(message):
    # Accept the connection
    message.reply_channel.send({"accept": True})
    # Add to the chat group
    Group("all").add(message.reply_channel)
    Group("user-{}".format(message.user.username)).add(message.reply_channel)


# Connected to websocket.receive
def ws_message(message):
    Group("all").send({
        "text": "[user] %s" % message.content['text'],
    })


# Connected to websocket.disconnect
def ws_disconnect(message):
    Group("all").discard(message.reply_channel)


def send_message(dict_message, group='all'):
    Group(group).send({"text": json.dumps(dict_message)})


def send_message_to_user(dict_message, user):
    group = "user-{}".format(user.username)
    Group(group).send({"text": json.dumps(dict_message)})