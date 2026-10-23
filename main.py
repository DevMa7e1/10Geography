from flask import Flask, request, redirect, make_response, render_template
import random
from PIL import Image
Image.MAX_IMAGE_PIXELS = 233280000
from base64 import b64encode
from io import BytesIO

app = Flask(__name__)
mapoftheworld = Image.open('./data/map.jpg')
print("Preparing world map...")
halfsize = mapoftheworld.resize((mapoftheworld.width/2, mapoftheworld.height/2))
quartersize = mapoftheworld.resize((mapoftheworld.width/4, mapoftheworld.height/4))
print("Done!\n")

def request_image(box: tuple[int, int, int, int]):
    c = 22.5
    def get_safe_box(rx1, ry1, rx2, ry2):
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
        if x2 > mapoftheworld.width:
            xsub = x2-mapoftheworld.width
            x2 -= xsub
        if y2 > mapoftheworld.height:
                    ysub = y2-mapoftheworld.height
                    y2 -= ysub
        x1 -= xsub
        y1 -= ysub
        return int(x1), int(y1), int(x2), int(y2)
    box = get_safe_box(*box)
    cropped: Image.Image = mapoftheworld.crop(box)
    cropped.paste(Image.open('./static/pin.png'), (int(28*c), int(20*c)), Image.open('./static/pin.png'))
    cropped = cropped.resize((int(28*c), int(20*c)))
    s = BytesIO()
    cropped.save(s, format='jpeg')
    val = s.getvalue()
    s.close()
    return val

@app.route('/request_image')
def get_image():
    posx = int(request.args['x'])
    posy = int(request.args['y'])
    zoom = float(request.args['z'])
    box = (int(posx-28*zoom), int(posy-20*zoom), int(posx+28*zoom), int(posy+20*zoom))
    image = request_image(box)
    return 'data:image/jpeg;base64,'+b64encode(image).decode()

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
    
    box = (int(pos[0])-28, int(pos[1])-20, int(pos[0])+28, int(pos[1])+20)
    image = request_image(box)
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