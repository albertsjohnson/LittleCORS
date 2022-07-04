import os
import re
import requests

url = 'http://www.tecnicarobertorocca.edu.ar/wp-json/'
headers = {
'Origin':'https://www.haha.com',
'Cookie':'wordpress_test_cookie=WP%20Cookie%20check',
'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
'Accept-Encoding':'gzip,deflate',
'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36',
'Host':'www.tecnicarobertorocca.edu.ar',
'Connection':'Keep-alive',
}
res = requests.get(url, headers=headers)
print(res.headers)
file = open("wp-json.api", mode="w+", encoding="utf-8")
file.write(res.text)
file.flush()
file.close()

results = re.findall('http:.*?"', res.text)
index = 0

results.sort()

for result in results:
    #if index < 36:
    #    index += 1
    #    continue
    result = result.replace('\\', '');
    result = result[:-1]
    print(result)
    if result.find('ar/') <= 0:
        continue
    dir_path = result[result.index('ar/')+3:result.rindex('/')]
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
    file_path = result[result.index('ar/')+3:]
    if os.path.exists(file_path) and os.path.isdir(file_path):
        file_path += ".txt"
    file = open(file_path + '.cors', mode="w+", encoding="utf-8")
    file.write(res.text)
    file.flush()
    file.close()
    print(f'{index} ({len(results)})')
    index = index + 1
    