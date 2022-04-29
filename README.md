# tgsint-bot
[!!under heavy development!!]

tgsint is a OSINT and pentesting telegram bot written in python.

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

Visit [Shodan](https://developer.shodan.io/) to obtain your API Key.

Visit [Zoomeye](https://zoomeye.org/) to obtain your API Key.

Change `"1234567890|123456789"` to your own telegram account id/s or simply remove user filter at the dispatcher if you want your bot to be accessible by everyone.  
This part filters messages to allow only those which are from specified user ID(s).

## Usage

```bash
Execute main.py  

TELEGRAM BOT:
/help to show available commands
```

## Features

1. Phone number lookup trough [tgsint-api](https://github.com/runtimeterrorist/tgsint-api).
2. Name & Surname lookup trough [tgsint-api](https://github.com/runtimeterrorist/tgsint-api).
3. WHOIS lookup trough [tgsint-api](https://github.com/runtimeterrorist/tgsint-api).
4. Associated domain names search via Zoomeye.
5. Shodan host search (gathers host IP address,CVE data and open ports).
6. Lookup information on bosnian car licence plates.
7. Lookup information on croatian car licence plates(tehnical examination and insurance details).
8. Shodan host geoip lookup.
9. Nmap quick scan (-sP) / custom scan

## Changelog

Check the changelog file

## Contributing

Pull requests are welcome.
If you have a suggestion open an issue with the tag "enhancement".  

## Legal disclaimer:
Developers assume no liability and are not responsible for any misuse or damage caused by this program.
This program is for educational purposes.

## License
[MIT](https://choosealicense.com/licenses/mit/
