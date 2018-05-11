#! /usr/bin/env python

from __future__ import print_function
import os

cwd = os.path.dirname(__file__)
img_dir = os.path.join(cwd, '../sample_imgs/')
tmp_zip_pathname = os.path.join(img_dir,'tmp_imgs.zip')

# http://stackoverflow.com/a/5032238
def ensure_path_exists(path):
    import errno

    try:
        os.makedirs(path)
    except OSError as exception:
        if exception.errno != errno.EEXIST:
            raise

def dl_img_zip():
    import requests

    print('Downloading sample images zip...')

    img_album_url = 'http://imgur.com/a/SOIUE/zip'
    chunk_size = 1024*1024

    r = requests.head(img_album_url)
    file_size = int(r.headers['content-length'])

    r = requests.get(img_album_url, stream=True)

    fmt_file_size = '{:.2f}'.format(file_size/(1024*1024))

    ensure_path_exists(img_dir)

    file_index = 0
    with open(tmp_zip_pathname, 'wb') as fd:
        for chunk in r.iter_content(chunk_size):
            fmt_file_index = '{:.2f}'.format(file_index/(1024*1024))
            print(fmt_file_index+'/'+fmt_file_size+' MB', end='\r')
            fd.write(chunk)
            file_index += chunk_size
    print(fmt_file_size+'/'+fmt_file_size+' MB')

    print('done')

def extract_sample_imgs():
    import zipfile

    print('Extracting sample images... ', end='\r')

    with zipfile.ZipFile(tmp_zip_pathname, 'r') as zip_ref:
        zip_ref.extractall(img_dir)

    print('Extracting sample images... done')

def rm_tmp_zip():
    print('Removing temporary zip file... ', end='\r')

    os.remove(tmp_zip_pathname)

    print('Removing temporary zip file... done')

if __name__ == '__main__':
    dl_img_zip()
    extract_sample_imgs()
    rm_tmp_zip()
