#!/usr/bin/env python
import json
from csv import reader as csvreader

import responder
import httpx
import environ

SRCDIR = environ.Path(__file__) - 1  # ./

env = environ.Env()
env.read_env(SRCDIR('env-local'))

if 'CSV_PAIRS_URL' in env:
    response = httpx.get(env('CSV_PAIRS_URL').strip(), timeout=25)
    codes = dict(csvreader(response.text.splitlines(), delimiter=','))
    #codes = dict(csvreader('a,b\nc,d'.splitlines(), delimiter=','))
        
app = responder.API()

@app.route("/")
async def home(req, resp):
    resp.content = app.template('home.html')

@app.route("/getvalue/{key}")
async def get(req, resp, *, key: str):
    resp.text = codes.get(key)
            
if __name__ == '__main__':
    app.run(debug=env.bool('WEB_DEBUG', default=False), port=env('PORT', default=8000))
