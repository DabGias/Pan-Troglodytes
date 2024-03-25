import os
from dotenv import load_dotenv

from bot import bot
from webserver import keep_alive

if __name__ == '__main__': 
    keep_alive()

    load_dotenv()

    bot.run(os.getenv("DISCORD_TOKEN_SECRET"))
