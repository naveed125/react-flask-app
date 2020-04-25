import random
from flask import Flask, request
from pymongo import MongoClient

app = Flask(__name__)


@app.route('/')
def index():
    return 'OK'


@app.route('/quote')
def quote():

    app.logger.info(f"ENTERING: {request.path}")

    client = MongoClient('db')
    db = client.quotesdb
    data = list(db.quotes.find())

    if len(data) < 1:
        return {
            "id": 0,
            "quote": "Remember to init the db with InitDB.js"
        }

    row = random.choice(data)
    return {
        "id": int(row['id']),
        "quote": row['quote']
    }


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
