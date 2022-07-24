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

Change `"1234567890|123456789"` to your own telegram account id/s or simply remove user filter at the dispatcher if you want your bot to be accessible by everyone.  
This part filters messages to allow only those which are from specified user ID(s).

## Usage

```bash
Execute main.py  

TELEGRAM BOT:
/help to show available commands
```

## Features

1. Phone number lookup.
2. Name & Surname lookup.
3. WHOIS lookup.
4. Subdomains lookup (uses nmap --script hostmap-crtsh).
5. Shodan host search (gathers host IP address,CVE data and open ports).
6. Lookup information on bosnian car licence plates.
7. Lookup information on croatian car licence plates(tehnical examination and insurance details).
8. Shodan host geoip lookup.
9. Nmap scans

[tgsint-api](https://github.com/runtimeterrorist/tgsint-api) serves most of the data for the bot.
## Changelog

Check the changelog file


## USEFUL NOTES:
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
