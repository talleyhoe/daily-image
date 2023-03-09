# This file needs to search/scrape images under 800kB

import json
import os, sys
from random import choice
from random import getrandbits, randrange
from urllib.parse import urlparse
import requests
import filetype

DEBUG = False

headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/110.0'}

def check_size(path: str):
    max_size = 800 * (1 << 10) # 800kB
    return ( os.path.getsize(path) <= max_size )
    
def sanitize_query(query: str):
    return query.replace(' ','+')

# Get a list of url sources and google's id tag for each image
def get_image_map(query):
    query = sanitize_query(query)
    all_images = {}

    chunk = 0
    step = 0
    prev_len = 0
    no_more = 0
    err_cnt = 0
    try_limit = 3
    
    while True:
        r = requests.get(f'https://www.google.com/search?q={query}&tbm=isch&biw=1271&bih=697&async=_id:islrg_c,_fmt:json&asearch=ichunklite&ved=0ahUKEwjw_KTXkM_3AhVJxDgGHR-pDeoQtDIIPSgA&start={chunk}&ijn={step}', headers=headers)
        
        if (r.status_code == 200):
            json_text = r.content.decode('utf8').removeprefix(")]}'")
            json_data = json.loads(json_text)
            try:
                results = json_data['ichunklite']['results']
                for result in results:
                    original_image = result['viewer_metadata']['original_image']['url']
                    all_images[original_image] = result['image_docid']

            except Exception as err:
                err_cnt += 1
                if err_cnt > 10:
                    sys.exit(1)
                if DEBUG:
                    print(err)
                    print("Issue requesting web page")
                
            chunk += 100
            step += 1   
        
        if (no_more > try_limit):
            return all_images
        if (prev_len == len(all_images)):
            no_more+=1
        else:
            prev_len = len(all_images)
            no_more = 0
            if DEBUG:
                print(len(all_images))

def download_image(url: str, file_path: str):
    try:
        response = requests.get(url, headers=headers)
    except Exception as err:
        print(err)
        print(f"Error requesting: {url}")
        return 1

    if response.status_code == 200:
        if "image" in response.headers.get("content-type", '').lower():
            with open(file_path, 'wb') as img:
                img.write(response.content)
            return 0
        else:
            return 1
    else:
        print(f"Error, Status Code: {response.status_code} for {url}")
        return 1

def get_image(usr_profile: list[str]):
    if not os.path.exists("../images"):
        os.mkdir("../images")
    query = choice(usr_profile)
    url_mapping = get_image_map(query)
    
    img_urls = list(url_mapping.keys())
    img_ids = list(url_mapping.values())
    id_cnt = len(img_ids)

    for attempt in range(id_cnt):
        # Get a random image
        idx = randrange(id_cnt)
        img_id = img_ids.pop(idx)
        img_url = img_urls.pop(idx)
        id_cnt -= 1

        file_path = f"../images/{img_id}"
        download_err = download_image(img_url, file_path)
        if download_err:
            continue

        valid_size = check_size(file_path)
        if valid_size:
            img_type = filetype.guess(file_path).mime.split('/')[-1]
            os.rename( file_path, '.'.join((file_path, img_type)) )

            file_path = '.'.join((file_path.split('/')[-1], img_type))
            return file_path

def test():
    global DEBUG
    DEBUG = True
    linux_profile = ["tux linux", "arch btw", "gentoo"]
    user_query = {
        "user": "talleyhoe",
        "profile": linux_profile
    }
    
    manifest_name = get_image(linux_profile)
    manifest = {
        user_query['user']: manifest_name
    }
    print(manifest)

    return 0


if __name__ == "__main__":
    test()
