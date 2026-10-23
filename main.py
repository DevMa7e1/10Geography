from flask import Flask, request, redirect, make_response, render_template
import random
from PIL import Image
Image.MAX_IMAGE_PIXELS = 233280000
from base64 import b64encode
from io import BytesIO

app = Flask(__name__)
mapoftheworld = Image.open('./data/map.jpg')

@app.route('/select')
def select():
    f = open('respond.html')
    r = f.read()
    f.close()
    cookies = request.headers.get('Cookie').split(';')
    for i in cookies:
        if i.split('=')[0].removeprefix(' ') == 'answer':
            cookies.remove(i)
    chosen = []
    for i in range(4):
        choice = random.choice(cookies)
        while choice in chosen and len(cookies) >= 4:
            choice = random.choice(cookies)
        chosen.append(choice)
        r = r.replace(f'%ch{i}', choice.split('=')[0].removeprefix(' '))
    answer = random.choice(chosen)
    pos = answer.split('=')[1].split('l')
    c = 22.5
    box = (int((int(pos[0])-28)*c), int((int(pos[1])-20)*c), int((int(pos[0])+28)*c), int((int(pos[1])+20)*c))
    cropped = mapoftheworld.crop(box)
    cropped.paste(Image.open('./static/pin.png'), (int(28*c), int(20*c)), Image.open('./static/pin.png'))
    cropped = cropped.resize((int(28*c), int(20*c)))
    s = BytesIO()
    cropped.save(s, format='jpeg')
    r = r.replace('mapimage', 'data:image/jpeg;base64,'+b64encode(s.getvalue()).decode())
    rp = make_response(r)
    rp.set_cookie('answer', answer.split('=')[0])
    return rp

@app.route('/add_location')
def add_loc():
    r = make_response(redirect('/manage_locations'))
    name = request.args['name']
    x = request.args['xpos']
    y = request.args['ypos']
    r.set_cookie(name, f"{x}l{y}")
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

@app.route('/check')
def check():
    cookies = request.headers.get('Cookie').split(';')
    correct = ''
    for i in cookies:
        if i.split('=')[0].removeprefix(' ') == 'answer':
            correct = i.split('=')[1].removeprefix('"').removesuffix('"')
    
    if correct.removeprefix(' ') == request.args['ch']:
        rp = make_response('Yay! Correct answer!<br><a href="/select"><button>Next</button></a>')
        rp.delete_cookie('answer')
        return rp
    else:
        rp = make_response('Wrong answer! It was actually '+correct+'.<br><a href="/select"><button>Next</button></a>')
        rp.delete_cookie('answer')
        return rp

app.run('0.0.0.0', 7555)