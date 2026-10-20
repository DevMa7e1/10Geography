from flask import Flask, request, redirect

app = Flask(__name__)

@app.route('/select')
def select():
    return request.headers.get('Cookie')

@app.route('/manage_locations')
def management():
    f = open('manage.html')
    r = f.read()
    f.close()
    return r

app.run('0.0.0.0', 7555)