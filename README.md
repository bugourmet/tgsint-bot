# tgsint 

tgsint is a OSINT telegram bot written in python for subdomain enumeration and facebook data leak search.

Facebook data leak is not provided in this repo,instead there's a sample.txt file which you can populate and use the telegram bot to search for results.
## Installation

1. Install necessary dependencies via pip
Install necessary dependencies.
```python
pip install -r requirements.txt
```
2. Create a Telegram bot using @botfather and place your bot token at this section.
```python
    bot = Updater("BOT_TOKEN")
```
3. Get a free API Key by signing up to [securitytrails](https://securitytrails.com) and put your API Key at this section. 
```python
    headers = {
        "Accept": "application/json",
        "APIKEY": "API_KEY"
    }
```
4. Change `"YOUR_ID"` at the dispatcher part (lines 68-69) to your own telegram account id or simply remove `"Filters.user(user_id=YOUR_ID)"` if you want your bot to be accessible by everyone.  
This part filters messages to allow only those which are from specified user ID(s).
## Usage


```bash
Execute main.py  

BOT:
/help to show available commands
```

## Contributing
Pull requests are welcome.
If you have a suggestion , please fork the repo and create a pull request. 

You can also simply open an issue with the tag "enhancement". 

## License
[MIT](https://choosealicense.com/licenses/mit/)
