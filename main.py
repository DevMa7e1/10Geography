from flask import Flask, request, redirect, make_response
import random

app = Flask(__name__)

@app.route('/select')
def select():
    cookies = request.headers.get('Cookie').split(';')
    return random.choice(cookies)

@app.route('/add_location')
def add_loc():
    r = make_response(redirect('/manage_locations'))
    name = request.args['name']
    location = request.args['pos']
    r.set_cookie(name, location)
    return r
@app.route('/remove')
def remove():
    name = request.args['name']
    r = make_response(redirect('/manage_locations'))
    r.set_cookie(name, expires='Thu, 01 Jan 1970 00:00:00 UTC')
    return r

@app.route('/manage_locations')
def management():
    f = open('manage.html')
    r = f.read()
    f.close()
    return r

app.run('0.0.0.0', 7555)