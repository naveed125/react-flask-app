import random
from flask import Flask

app = Flask(__name__)


@app.route('/')
def index():
    return 'OK'


@app.route('/quote')
def quote():
    return random.choice([
        "A hungry man may only think of the food",
        "Smart people have all the fun",
        "Hard to beat someone who doesn't give up",
        "Understanding yourself is the hardest thing in the world",
        "You may only change the future",
        "Choose habits over will power if you actually want to succeed"
    ])


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
