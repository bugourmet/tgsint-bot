# tgsint-bot

[![GitHub stars](https://img.shields.io/github/stars/runtimeterrorist/tgsint-bot.svg)](https://github.com/runtimeterrorist/tgsint-bot/stargazers)
[![GitHub license](https://img.shields.io/github/license/runtimeterrorist/tgsint-bot.svg)](https://github.com/runtimeterrorist/tgsint-bot/blob/master/LICENSE)
[![GitHub forks](https://img.shields.io/github/forks/runtimeterrorist/tgsint-bot.svg)](https://github.com/runtimeterrorist/tgsint-bot/network/members)
[![GitHub issues](https://img.shields.io/github/issues/runtimeterrorist/tgsint-bot.svg)](https://github.com/runtimeterrorist/tgsint-bot/issues)
[![GitHub pull requests](https://img.shields.io/github/issues-pr/runtimeterrorist/tgsint-bot.svg)](https://github.com/runtimeterrorist/tgsint-bot/pulls)
[![GitHub last commit](https://img.shields.io/github/last-commit/runtimeterrorist/tgsint-bot.svg)](https://github.com/runtimeterrorist/tgsint-bot/commits/master)

tgsint is a OSINT telegram bot written in python.

## Installation

Install necessary dependencies via pip
Install necessary dependencies.

```python
pip install -r requirements.txt
```

Set up [tgsint-api](https://github.com/runtimeterrorist/tgsint-api).

## Configuration

#### Open `.env` file and add required keys/tokens...

Create a Telegram bot using @botfather and get your bot token.

Change USERS`"1234567890|123456789"` to your own telegram account id/s or simply remove user filter at the dispatcher if you want your bot to be accessible by everyone.  
This part filters incoming messages (commands) from users with above specified IDs.

## Usage

```bash
Execute main.py

TELEGRAM BOT:
/help to show available commands
```

## Features

1. Phone number lookup.
2. Name & Surname lookup.
3. Lookup information on croatian car licence plates.

## Changelog

Check the changelog file

## NOTES:

In some cases people have their middle name set on their profile page.
Finding them works the same way as for other people , middle name is excluded in the search query.

## Contributing

Pull requests are welcome.
If you have a suggestion open an issue with the tag "enhancement".

## Legal disclaimer:

Developers assume no liability and are not responsible for any misuse or damage caused by this program.
This program is for educational purposes.

## License

[MIT](https://choosealicense.com/licenses/mit/)
