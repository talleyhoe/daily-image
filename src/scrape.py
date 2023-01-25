# This file needs to search/scrape images under 300kB

import os, sys
from random import choice, getrandbits, randrange
from urllib import request

import filetype
from bs4 import BeautifulSoup

def check_size(path: str):
    max_size = 300 * (1 << 10) # 300kB
    return ( os.path.getsize(path) <= max_size )
    
def sanitize_keyword(keyword: str):
    return keyword.replace(' ','+')

def search_image(keyword: str):
    headers = {'User-Agent': 'Mozilla/5.0'}
    search_url = f"https://www.google.com/search?q={keyword}&tbm=isch"
    search_request = request.Request(search_url, headers=headers)
    try:
        return request.urlopen(search_request).read().decode('utf-8')
    except Exception as err:
        print(err)
        print("Issue requesting web page")
        sys.exit(1)

def get_urls(profile: list[str]):
    keyword = sanitize_keyword( choice(profile) )
    response = search_image(keyword)
    soup = BeautifulSoup(response, 'html.parser')
    return soup.find_all('img', {'class': 'yWs4tf'})


def get_image(url_tags: list[str], file_path: str):
    tag_cnt = len(url_tags)
    for attempt in range(tag_cnt):
        idx = randrange(tag_cnt)
        tag_attempt = url_tags.pop(idx)
        tag_cnt -= 1

        request.urlretrieve(tag_attempt.get('src'), file_path) # download image

        valid_size = check_size(file_path)
        if valid_size:
            img_type = filetype.guess(file_path).mime.split('/')[-1]
            os.rename( file_path, '.'.join((file_path, img_type)) )

            manifest_name = '.'.join((file_path.split('/')[-1], img_type))
            return manifest_name

def gen_path(folder="../images"):
    bit_range = 32
    collision = True
    while collision:
        file_id = str(getrandbits(bit_range)) # becuase python is silly
        path = '/'.join((folder, file_id))
        collision = os.path.isfile(path)
    return path


def test():
    linux_profile = ["tux linux", "arch btw", "gentoo"]
    user_query = {
        "user": "talleyhoe",
        "profile": linux_profile
    }
    
    img_folder = "../test"
    img_path = gen_path(img_folder)

    img_urls = get_urls(linux_profile)
    manifest_name = get_image(img_urls, img_path)
    maifest = {
        user_query['user']: manifest_name
    }

    return 0


if __name__ == "__main__":
    test()
