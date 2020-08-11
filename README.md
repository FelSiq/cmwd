# Call Me When Done (MCWD)
Send a Telegram message to me when done executing my Python script.

## Configure
If you don't have a secret bot token already, follow [this Telegram official guide](https://core.telegram.org/bots#6-botfather) in order to get one.

Open the `cmwd.py` script and set up your bot name and secret key in the `bot_name` and `secret_token` variables, respectively.

You also need to configure your telegram username in the `my_telegram_username` variable.

```python
bot_name = "my_bot"
secret_token = "1234abcde0987abdkfhh038ufsd"
my_telegram_username = "my_username"
```

Then you're done!

## Usage
Run `cmwd.py` script with your Python interpreter passing your main script as the first argument. You can pass additional arguments as many as you need to your main script.
```bash
python cmwd.py <script> [args...]
```
