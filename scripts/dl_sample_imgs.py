#! /usr/bin/env python

#from __future__ import print_function
#from __future__ import absolute_import
from __future__ import print_function
import os
import errno
import requests
import zipfile

#ROOT_DIR = '/home/josh/r/golfr'
from golfr.utils import ensure_path_exists




def dl_img_zip(img_dir, tmp_zip_pathname):

    print('Downloading sample images zip to "{}" ...'.format(img_dir))

    # link expired :/ ... imgur has betrayed me
    #IMG_ALBUM_URL = 'http://imgur.com/a/SOIUE/zip'
    IMG_ALBUM_URL = 'https://drive.google.com/uc?export=download&id=0B01ArorP31gEbi1sSnE0aFZVYU0' 
    CHUNK_SIZE = 1024*1024
    
    

    #r = requests.head(IMG_ALBUM_URL)
    #file_size = int(r.headers['content-length'])

    r = requests.get(IMG_ALBUM_URL, stream=True)

    #fmt_file_size = '{:.2f}'.format(file_size/CHUNK_SIZE)

    ensure_path_exists(img_dir)

    file_index = 0
    with open(tmp_zip_pathname, 'wb') as fd:
        print('0.0 MB', end='\r')
        for chunk in r.iter_content(CHUNK_SIZE):
            file_index += len(chunk)
            fmt_file_index = '{:.2f}'.format(file_index/CHUNK_SIZE)
            print(fmt_file_index+' MB', end='\r')
            fd.write(chunk)
    print()
    print('done')

def extract_sample_imgs(tmp_zip_pathname):

    print('Extracting sample images ... ', end='\r')
    
    with zipfile.ZipFile(tmp_zip_pathname, 'r') as zip_ref:
        zip_ref.extractall(img_dir)

    print('Extracting sample images ... done')

if __name__ == '__main__':
    img_dir = os.path.abspath('../imgs/') #os.path.join(ROOT_DIR, 'sample_imgs/')
    tmp_zip_pathname = os.path.join(img_dir,'sample_imgs.zip')
    
    dl_img_zip(img_dir, tmp_zip_pathname)
    extract_sample_imgs(tmp_zip_pathname)
    os.remove(tmp_zip_pathname)
