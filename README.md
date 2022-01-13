# tgsint 

tgsint is a OSINT telegram bot written in python for subdomain enumeration and facebook data leak search.

Facebook data leak is not provided in this repo,instead there's a sample.txt file which you can populate and use the telegram bot to search for results.
## Installation

Install necessary dependencies via pip
Install necessary dependencies.
```python
pip install -r requirements.txt
```
## Configuration
#### Open `config.py` and add required keys/tokens...

Create a Telegram bot using @botfather and get your bot token.

Get a free API Key by signing up to [SecurityTrails](https://securitytrails.com)

Visit [Shodan](https://developer.shodan.io/) to obtain your API Key.

Change `"1234567890"` to your own telegram account id or simply remove `"Filters.user(user_id=YOUR_ID)"` if you want your bot to be accessible by everyone.  
This part filters messages to allow only those which are from specified user ID(s).
## Usage


```bash
Execute main.py  

TELEGRAM BOT:
/help to show available commands
```

## Features
1. Query trough given text dataset
2. Check for subdomains associated with target domain name.
3. WHOIS Lookup
4. Shodan host search (gathers host IP address,CVE data and open ports)

#### TODO:
```bash
- error handling
- port scanning
- bot response formatting
- clean up the code
```

## Contributing
Pull requests are welcome.
If you have a suggestion , please fork the repo and create a pull request. 

You can also simply open an issue with the tag "enhancement". 

## License
[MIT](https://choosealicense.com/licenses/mit/)
