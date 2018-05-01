import os

img_dir = '../sample_imgs/'
tmp_zip_pathname = os.path.join(img_dir,'tmp_imgs.zip')

def dl_img_zip():
    import requests
    img_album_url = 'http://imgur.com/a/SOIUE/zip'
    r = requests.get(url, stream=True)

    with open(tmp_zip_pathname, 'wb') as fd:
        for chunk in r.iter_content(chunk_size):
            fd.write(chunk)

    print('Successfully downloaded sample images zip.')

def extract_sample_imgs():
    import zipfile
    with zipfile.ZipFile(tmp_zip_pathname, 'r') as zip_ref:
        zip_ref.extractall(img_dir)

    print('Successfully extracted sample images.')

def rm_tmp_zip():
    os.remove(tmp_zip_pathname)

    print('Successfully removed temporary zip file.')
if __name__ == '__main__':
    dl_img_zip()
    extract_sample_imgs()
    rm_tmp_zip()
