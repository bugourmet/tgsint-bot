def splitmessage(message):
    message_list = []
    if len(message) > 4096:
        for x in range(0, len(message), 4096):
            message_list.append(message[x:x+4096])
    else:
        message_list.append(message)
    return message_list


def sendmessage(reply,update):
    messages = splitmessage(reply)
    for message in messages:
        update.message.reply_text(message,parse_mode='Markdown')