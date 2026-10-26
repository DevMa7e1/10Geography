from flask import Flask, request, redirect, make_response
import random
import pyvips
from base64 import b64encode
from gc import collect

app = Flask(__name__)
mapoftheworld = pyvips.Image.new_from_file('data/map.jpg', access="random", memory=True)

def request_image(box: tuple[int, int, int, int], zoom: float = 1.0):
    global mapoftheworld
    c = 11.25
    def get_safe_box(rx1, ry1, rx2, ry2, image):
        x1 = rx1*c; y1 = ry1*c; x2 = rx2*c; y2 = ry2*c
        xadd = 0
        yadd = 0
        if x1 < 0:
            xadd = 0-x1
            x1 += xadd
        if y1 < 0:
            yadd = 0-y1
            y1 += yadd
        x2 += xadd
        y2 += yadd
        xsub = 0
        ysub = 0
        if x2 > image.width:
            xsub = x2-image.width
            x2 -= xsub
        if y2 > image.height:
                    ysub = y2-image.height
                    y2 -= ysub
        x1 -= xsub
        y1 -= ysub
        return (int(x1), int(y1), int(x2)-int(x1), int(y2)-int(y1)), xadd-xsub, yadd-ysub
    box, xof, yof = get_safe_box(*box, mapoftheworld)
    cropped: pyvips.Image = mapoftheworld.crop(*box)
    pin = pyvips.Image.new_from_file('./static/pin.png')
    pin = pin.resize(zoom*(0.4))
    cropped = cropped.composite(pin, 'over', x=(int(cropped.width/2-xof)), y=int(cropped.height/2-yof))
    val = cropped.write_to_buffer('.jpg[Q=50]')
    del pin
    del cropped
    collect()
    return val

@app.route('/request_image')
def get_image():
    posx = int(request.args['x'])
    posy = int(request.args['y'])
    zoom = float(request.args['z'])
    box = (int(posx-28*zoom), int(posy-20*zoom), int(posx+28*zoom), int(posy+20*zoom))
    image = request_image(box, float(zoom))
    return 'data:image/jpeg;base64,'+b64encode(image).decode()

@app.route('/request_full')
def get_full():
    f = open('data/map.jpg', 'rb')
    val = f.read()
    f.close()
    return 'data:image/jpeg;base64,'+b64encode(val).decode()
@app.route('/select')
def select():
    f = open('respond.html')
    r = f.read()
    f.close()
    cookie = request.headers.get('Cookie')
    if type(cookie) == str:
        cookies = cookie.split(';')
    else:
        cookies = []
    c = cookies.copy()
    for i in c:
        if 'answer' in i:
            cookies.remove(i)
        if '_' in i:
            cookies.remove(i)
    if cookies == []:
        rp = make_response("Error 400:\nPlease add at least one location. <a href='/manage_locations'><button>Go back</button></a>")
        rp.status_code = 400
        return rp
    chosen = []
    for i in range(4):
        choice = random.choice(cookies)
        while choice in chosen and len(cookies) >= 4:
            choice = random.choice(cookies)
        chosen.append(choice)
        r = r.replace(f'%ch{i}', choice.split('=')[0].removeprefix(' '))
    answer = random.choice(chosen)
    pos = answer.split('=')[1].split('l')
    
    box = (int(int(pos[0])-28*float(pos[2])/10), int(int(pos[1])-20*float(pos[2])/10), int(int(pos[0])+28*float(pos[2])/10), int(int(pos[1])+20*float(pos[2])/10))
    image = request_image(box, float(pos[2])/10)
    r = r.replace('mapimage', 'data:image/jpeg;base64,'+b64encode(image).decode())
    rp = make_response(r)
    rp.set_cookie('answer', answer.split('=')[0])
    return rp

@app.route('/add_location')
def add_loc():
    r = make_response(redirect('/manage_locations'))
    name = request.args['name']
    x = request.args['xpos']
    y = request.args['ypos']
    z = request.args['zpos']
    r.set_cookie(name, f"{x}l{y}l{z}")
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
    f = open('answer.html')
    r = f.read()
    f.close()
    if len(request.args.keys()) > 0:
        cookie = request.headers.get('Cookie')
        if type(cookie) == str:
            cookies = cookie.split(';')
        else:
            cookies = []
        correct = ''
        for i in cookies:
            if i.split('=')[0].removeprefix(' ') == 'answer':
                correct = i.split('=')[1].removeprefix('"').removesuffix('"')

        if correct.removeprefix(' ') == request.args['ch']:
            r = r.replace('%ans', ' correct!').replace('%cor', '')
            rp = make_response(r)
            rp.delete_cookie('answer')
            return rp
        else:
            r = r.replace('%ans', ' wrong.').replace('%cor', f'Correct answer: {correct}')
            rp = make_response(r)
            rp.delete_cookie('answer')
            return rp
    else:
        r = r.replace('%ans', ': pass.').replace('%cor', f'No answer has been given.')
        rp = make_response(r)
        rp.delete_cookie('answer')
        return rp

@app.route('/favicon.ico')
def favicon():
    f = open('favicon.ico', 'rb')
    r = f.read()
    f.close()
    return r

@app.route('/')
def main():
    f = open('index.html')
    r = f.read()
    f.close()
    return r