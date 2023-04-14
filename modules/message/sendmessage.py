def splitmessage(message):
    """Function used for splitting long messages (4096 char/message limit)"""
    message_list = []
    if len(message) > 4096:
        for num in range(0, len(message), 4096):
            message_list.append(message[num:num+4096])
    else:
        message_list.append(message)
    return message_list


def sendmessage(reply, update):
    """Send telegram message function"""
    messages = splitmessage(reply)
    for message in messages:
        update.message.reply_text(message, parse_mode='Markdown')
