import os
from dotenv import dotenv_values
from bot import bot

if __name__ == '__main__':
    values = dotenv_values(".env")
    bot.run(values["DISCORD_TOKEN_SECRET"] or os.getenv("DISCORD_TOKEN_SECRET"))
