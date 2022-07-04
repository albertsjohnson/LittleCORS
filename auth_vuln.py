import os
import re
import requests
import time

base_url = input("Input URL:    ")
base_dir = input("Store Path:   ")
if not os.path.exists(base_dir):
    os.mkdir(base_dir)
last_two_chars = base_url[-2:]

url = f'http://{base_url}/wp-json/'

headers = {
'Origin':'https://www.hellokit.com',
'Cookie':'wordpress_test_cookie=WP%20Cookie%20check',
'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
'Accept-Encoding':'gzip,deflate',
'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36',
'Host':base_url,
'Connection':'Keep-alive',
}
res = requests.get(url, headers=headers)
print(res.headers)
file = open(f"{base_dir}/wp-json.api", mode="w+", encoding="utf-8")
file.write(res.text)
file.flush()
file.close()

results = re.findall('http.*?"', res.text)
index = 0

results.sort()

for result in results:
    #if index < 36:
    #    index += 1
    #    continue
    result = result.replace('\\', '');
    result = result[:-1]
    print(result)
    if result.find(f'{last_two_chars}/') <= 0:
        continue
    dir_path = result[result.index(f'{last_two_chars}/')+3:result.rindex('/')]
    dir_path = base_dir + "/" + dir_path
    print(dir_path)
    if os.path.isfile(dir_path):
        os.rename(dir_path, dir_path + '.txt')
        os.makedirs(dir_path)
    res = requests.get(result, headers=headers)
    if not os.path.exists(dir_path):
        print(dir_path)
        os.makedirs(dir_path)
    

    #print(result[-1:-1])
    if result[-1:] == '/':
        result += 'backslash.api'
    file_path = result[result.index(f'{last_two_chars}/')+3:]
    file_path = base_dir + "/" + file_path
    if os.path.exists(file_path) and os.path.isdir(file_path):
        file_path += ".txt"
    file = open(file_path + '.cors', mode="w+", encoding="utf-8")
    file.write(res.text)
    file.flush()
    file.close()
    print(f'{index} ({len(results)})')
    index = index + 1
    