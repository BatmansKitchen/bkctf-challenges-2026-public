from flask import Flask, request, render_template, send_file
from secrets import token_hex
from os import path, getcwd
from werkzeug import utils


app = Flask(__name__)
key = token_hex(16)
assets = path.abspath('assets')
other = path.abspath('other')
print (assets)

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/blog/<int:blog>')
def blogs(blog):
    if blog >= 1 and blog < 5:
        return render_template(f'blog_{blog}.html', key=key)
    print ('invalid blog')
    return render_template('404.html'), 404

@app.route('/attachment')
def attachment():
    file = request.args.get('file')
    if not request.args.get('apiKey'): user_key = 0
    else: user_key = request.args.get('apiKey')
    if not user_key == key and utils.safe_join(assets, file) is None:
        return render_template('403.html'), 403
    else:
        if user_key == 0:
            print (path.join(assets, file))
            if not path.isfile(path.join(assets, file)): return render_template('404.html'), 404
            return send_file(path.join(assets, file))
        else:
            print (path.join(other, file))
            if not path.isfile(path.join(other, file)): return render_template('404.html'), 404
            return send_file(path.join(other, file))


if __name__ == '__main__':
    with open('/flag.txt', 'w') as f:
        f.write('bkctf{k3ys_in_th3_l0ck5}')
    # start on whatever the fuck
    app.run(host='0.0.0.0')