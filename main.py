import os
from dotenv import load_dotenv

from bot import bot


if __name__ == '__main__': 
    load_dotenv()
    token: str | None = os.getenv("DISCORD_TOKEN_SECRET")

    if token is not None:
        bot.run(token)
    else:
        print("Token inválido!")
