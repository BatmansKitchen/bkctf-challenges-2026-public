from flask import Flask, request, make_response, render_template, redirect
from random import randint


flag = "bkctf{y0ure_g0nn4_g3t_th3_h0rns}"
key_arr = ['abbaab', 'abaaab', 'abbaaa', 'aabaab', 'ababba', 'aaaaba', 'aaabaa', 'bbbbbbb', 'aabaaa', 'aababb', 'ababbba', 'abbabb', 'ababab', 'bbbbbbb', 'aabbbba', 'aabbbba', 'bbbbaa', 'abbabb', 'ababab', 'bbbbab', 'aabaab', 'abbabb', 'aabaab', 'ababaa', 'bbbbab', 'abbabb', 'ababaa', 'bbbbbbb', 'aababb', 'aabbbba', 'aababa', 'aaaaaa']
app = Flask(__name__)
legal = '0123456789@ABCDEFGHIJKLMNOPQRSTUVWXYZ[]^_abcdefghijklmnopqrstuvwxyz{|}'
MIN = 0
MAX = len(legal) - 1

def ord(c):
    return legal.index(c)    

def chr(i):
    return legal[i]

print (ord('b'))

def getletter(target):
    c = randint(MIN, MAX - 2)
    if c % 2 != (target % 2): c += 1
    return chr(c)

def search(key):
    low = MIN
    high = MAX

    for move in key:
        mid = (low + high) // 2

        print (low, mid, high)
        if ord(move) % 2 == 0:
            high = mid
        elif ord(move) % 2 == 1:
            low = mid + 1
        else:
            raise ValueError('fuck')

    if low != high:
        return -1
    return low

def move(request, i, direction):
    key = request.cookies.get('progress', default='')
    if len(key) + 1 > len(key_arr[i]): resp = make_response(redirect(f"/flag/{i}", 303))
    else: 
        index = key_arr[i][len(key)]
        if direction == ord(index) % 2: resp = make_response(redirect(f"/flag/{i}", 302))
        else: resp = make_response(redirect(f"/flag/{i}", 303))
    if direction % 2 == 0: cookie = getletter(ord('b'))
    else: cookie = getletter(ord('a'))
    resp.set_cookie('progress', key + cookie)
    return resp

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/flag/<int:i>')
def choice(i):
    key = request.cookies.get('progress', default='')
    print (key)
    res = search(key)
    print (chr(res))
    if len(key) > 10: raise ValueError('key too long')
    if res == -1: return render_template('choice.html', index=i)
    elif chr(res) == flag[i]: return render_template('success.html')
    else: return render_template('fail.html')

@app.route('/flag/<int:i>/left')
def left(i):
    return move(request, i, 0)

@app.route('/flag/<int:i>/right')
def right(i):
    return move(request, i, 1)

@app.route('/warning.txt')
def warning():
    return render_template('warning.txt')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)