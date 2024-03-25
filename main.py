import os
from dotenv import load_dotenv
from flask import Flask
from threading import Thread

from bot import bot

app = Flask(__name__)

@app.route("/")
def home():
    return "bot online"

def run():
    app.run(host="0.0.0.0", port=8080)

def keep_alive():
    t = Thread(target=run)
    
    t.start()
    

if __name__ == '__main__': 
    keep_alive()

    load_dotenv()

    bot.run(os.getenv("DISCORD_TOKEN_SECRET"))
