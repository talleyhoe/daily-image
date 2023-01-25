
from mail import *
from scrape import *

def main():
    user_query = {
        "user": "talleyhoe",
        "profile": ["tux linux", "arch btw", "gentoo"]
    }

    img_path = gen_path()
    img_urls = get_urls(user_query['profile'])
    manifest_name = get_image(img_urls, img_path)
    manifest = {
        user_query['user']: manifest_name
    }

    mail_txt(user_query['user'], "Test worked", "Txt test - subject")
    mail_image(user_query['user'], manifest)

if __name__ == "__main__":
    main()
