# Call Me When Done (MCWD)
Send a Telegram message to me when done executing my Python script.

## Configure
If you don't have a secret bot token already, follow [https://core.telegram.org/bots#6-botfather](this official Telegram guide) in order to get one.

Open the `cmwd.py` script and set up your bot name and secret key in the `bot_name` and `secret_token` variables, respectively.

```python
bot_name = "my_bot"
secret_token = "1234abcde0987abdkfhh038ufsd"
```

Then you're done!

## Usage
Run `cmwd.py` script with your Python interpreter passing your main script as the first argument. You can pass additional arguments as many as you need to your main script.
```bash
python cmwd.py <script> [args...]
```
