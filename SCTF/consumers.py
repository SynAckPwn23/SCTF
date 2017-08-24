from channels.auth import http_session_user

# In consumers.py
from channels import Group

# Connected to websocket.connect
@http_session_user
def ws_add(message):
    # Accept the connection
    message.reply_channel.send({"accept": True})
    # Add to the chat group
    print(message.user)
    Group("challenge-solved").add(message.reply_channel)
    Group("user-{}".format(message.user.username)).add(message.reply_channel)


# Connected to websocket.receive
def ws_message(message):
    Group("challenge-solved").send({
        "text": "[user] %s" % message.content['text'],
    })


# Connected to websocket.disconnect
def ws_disconnect(message):
    Group("challenge-solved").discard(message.reply_channel)


def send_message(text, group='challenge-solved'):
    Group(group).send({"text": text})


def send_message_to_user(text, user):
    group = "user-{}".format(user.username)
    Group(group).send({"text": text})