from flask import Flask, request, redirect, make_response, render_template
import random
from PIL import Image
Image.MAX_IMAGE_PIXELS = 233280000
from base64 import b64encode

app = Flask(__name__)
mapoftheworld = Image.open('./data/map.jpg')

@app.route('/select')
def select():
    f = open('respond.html')
    r = f.read()
    f.close()
    cookies = request.headers.get('Cookie').split(';')
    chosen = []
    for i in range(4):
        choice = random.choice(cookies)
        while choice in chosen and len(cookies) >= 4:
            choice = random.choice(cookies)
        chosen.append(choice)
        r = r.replace(f'%ch{i}', choice.split('=')[0])
    answer = random.choice(chosen)
    r = r.replace('%loc', answer.split('=')[1])
    rp = make_response(r)
    return rp

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
    r.delete_cookie(name)
    return r

@app.route('/manage_locations')
def management():
    f = open('manage.html')
    r = f.read()
    f.close()
    f = open('./data/thumbnail.jpg', 'rb')
    thumb = b64encode(f.read()).decode()
    f.close()
    r = r.replace('thumbnail-image', 'data:image/jpeg;base64,'+thumb)
    return r
app.run('0.0.0.0', 7555)