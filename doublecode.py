#!/usr/bin/env python
import json
from csv import reader as csvreader
from random import randint

import responder
import httpx
import environ
import redis


SRCDIR = environ.Path(__file__) - 1  # ./

env = environ.Env()
env.read_env(SRCDIR('env-local'))

db = redis.Redis.from_url(env('REDIS_URL'))

if 'CSV_PAIRS_URL' in env:
    response = httpx.get(env('CSV_PAIRS_URL').strip(), timeout=25)
    csv = csvreader(response.text.splitlines(), delimiter=',')
    codes = dict((key.replace('-', ''), val) for key, val in csv)
    #codes = dict(csvreader('a,b\nc,d'.splitlines(), delimiter=','))
        
app = responder.API()


@app.route("/")
async def home(req, resp):
    resp.content = app.template('home.html')


@app.route("/getvalue/{key}")
async def get(req, resp, *, key: str):
    key = key.replace('-', '')
    if key == 'test':
        resp.media = {'value': str(randint(0, 9999))}
    elif db.get(key) == b'obtained':
        resp.media = {'error': 'Этот код уже был использован'}
    else:
        value = codes.get(key)
        if value:
            db.set(key, 'obtained')  # Отметить как использованый.
        resp.media = {'value': value}

            
if __name__ == '__main__':
    app.run(debug=env.bool('WEB_DEBUG', default=False), port=env('PORT', default=8000))
