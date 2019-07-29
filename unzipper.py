import os
from zipfile import ZipFile
import shutil

zipfiles = []
to_unzip = []

for f in os.listdir('./'):
    if f.endswith('.zip'):
        zipfiles.append(f)

for f in zipfiles:
    if f.rstrip('.zip') not in os.listdir('./'):
        to_unzip.append(f)


for f in to_unzip:
    print('Unzipping {}'.format(f))
    with ZipFile('./' + f) as zipf:
        ar = zipf.namelist()
        fname = os.path.basename(ar[0])
        print(fname)
        source = zipf.open(ar[0])
        tar = open(os.path.join('./', fname), 'wb')
        with source, tar:
            shutil.copyfileobj(source, tar)
