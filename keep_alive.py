from flask import Flask, render_template
from threading import Thread
import main
#is_bot_running=False
app = Flask(__name__)
app.debug = True

@app.route('/')
def index():
  #if not is_bot_running:
  t = Thread(target=main.bot)
  t.start()
  #is_bot_running=True
  #return "Bot Started"
  return "Bot Alive"


def run():
  app.run(host='0.0.0.0', port=8080)


def keep_alive():
  #t = Thread(target=run)
  #t.start()
  run()
keep_alive()
