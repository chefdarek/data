import urllib.request
import uritools
import os

with open("./urls.list", 'r') as f:
    urls = [line.rstrip('\n') for line in f]

got_files = []
urls_to_get = []

for u in os.listdir('./'):
    if '.zip' in u:
        got_files.append(u)

for url in urls:
    if uritools.urisplit(url)[2].split('/')[-1] not in got_files:
        urls_to_get.append(url)


print('Already downloaded:\n')
for f in got_files:
    print(f)
print('Beginning Download...')

remaining = len(urls_to_get)

print('\n\n{} files left to download'.format(remaining))


for url in urls_to_get:

    name = uritools.urisplit(url)[2].split('/')[-1]

    print('downloading {}'.format(name))
    urllib.request.urlretrieve(url, name)
    remaining += -1
    print('Done. {} to go'.format(remaining))
    
