"""Send a message to telegram when my script finishes running."""
import sys
import requests
import os
import datetime

# --------------------------
# Configure these variables:
# --------------------------

# hint: don't put '@' at the start of the bot's name.
bot_name = ""

# hint: If you don't have your bot secret key, or didn't created your bot
# already, ask Telegram's @BotFather (here: https://t.me/botfather) for
# your secret token.
secret_token = ""  

# hit: usernames in Telegram are case-insensitive. Also, don't put '@' in
# front of your username.
my_telegram_username = ""

# --------------------------
# Now you're good to go!
# Run this script passing your main Python script as argument!
# You can also pass any number of extra arguments to your main script.
# --------------------------


my_telegram_username = my_telegram_username.lower()
python_alias = sys.executable
bot_url = "https://api.telegram.org/bot" + secret_token + "/"
bot_message = "Your script finished running."
datetime_format = "%d/%m/%Y %H:%M:%S"


def get_chat_id() -> str:
    """Get telegram chat ID."""
    my_chat_id = os.environ.get("CMWD_CHAT_ID")

    if my_chat_id is not None:
        print(
            f"Recovered chat id: {my_chat_id} from 'CMWD_CHAT_ID' environment variable."
        )
        return my_chat_id

    request_url = bot_url + "getUpdates"
    response = requests.get(request_url)

    try:
        # Search for the correct chat id, matching the configured Telegram username
        for msg in response.json()["result"]:
            username = msg["message"]["from"]["username"].lower()
            if username == my_telegram_username:
                my_chat_id = str(msg["message"]["chat"]["id"])
                break

    except KeyError:
        print(
            "You did not started a conversation with your bot. "
            f"Send a '/start' message to it in https://t.me/{bot_name}."
        )

        return None

    if my_chat_id is None:
        print("Unable to find your chat id. Did you configured your Telegram username "
              f"correctly ('{my_telegram_username}', is that you?) and have send a /start "
              "message to your bot already?")

        return None

    os.environ["CMWD_CHAT_ID"] = my_chat_id

    print(f"Got chat id: {my_chat_id}, and set to 'CMWD_CHAT_ID' environment variable.")

    return my_chat_id


def send_message(
    my_chat_id: str,
    ret_code: str,
    script_path: str,
    time_start: str,
    time_end: str,
    time_delta: str,
):
    """Send message to Telegram when script finishes."""
    request_url = (
        bot_url
        + "sendMessage?chat_id="
        + my_chat_id
        + "&parse_mode=Markdown&text="
        + bot_message
        + "\n\nScript path: "
        + script_path.replace("_", "\\_")
        + "\n\nStart time: "
        + time_start
        + "\nFinish time: "
        + time_end
        + "\nTotal time elapsed: "
        + time_delta
        + "\n\nExit code: "
        + ret_code
    )
    response = requests.get(request_url)
    return response.json()


def execute_script(script_path: str):
    """Execute a Python script."""
    return os.system(f"{python_alias} {script_path} " + " ".join(sys.argv[2:]))


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(f"usage: {python_alias}", sys.argv[0], "<python script path>")
        exit(1)

    if not bot_name:
        raise ValueError(
            "Bot name is not configured!\n"
            "Ask Telegram's BotFather for your bot name at "
            "https://t.me/botfather and then modify the "
            "'bot_name' variable."
        )

    if not secret_token:
        raise ValueError(
            "Bot secret token is not configured!\n"
            "Ask Telegram's BotFather for your bot secret token at "
            "https://t.me/botfather and then modify the "
            "'secret_token' variable."
        )

    script_path = sys.argv[1]

    my_chat_id = get_chat_id()

    if my_chat_id is None:
        exit(1)

    time_start = datetime.datetime.now()
    ret_code = execute_script(script_path)
    time_end = datetime.datetime.now()

    time_delta = time_end - time_start

    response = send_message(
        my_chat_id,
        str(ret_code),
        script_path,
        time_start.strftime(datetime_format),
        time_end.strftime(datetime_format),
        str(time_delta).split(".")[0],
    )

    if not response["ok"]:
        print("\nAn error occurred while sending the Telegram message:")
        print(response)
