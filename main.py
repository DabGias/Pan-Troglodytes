import os
from dotenv import load_dotenv
from flask import Flask
from threading import Thread
from http.server import BaseHTTPRequestHandler

from bot import bot

class handler(BaseHTTPRequestHandler):
 
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type','text/plain')
        self.end_headers()
        self.wfile.write("bot online!".encode('utf-8'))

        app = Flask(__name__)

        def run():
            app.run(host="0.0.0.0", port=8080)

        def keep_alive():
            t = Thread(target=run)
            
            t.start()
            

        if __name__ == '__main__': 
            keep_alive()

            load_dotenv()

            bot.run(os.getenv("DISCORD_TOKEN_SECRET"))

