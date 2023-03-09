
from mail import *
from scrape import *

def main():
    user_query = {
        "user": "talleyhoe",
        "profile": ["tux linux", "arch btw", "gentoo"],
        "subject": "Txt test - subject",
        "body": "Test worked",
    }

    manifest_name = get_image(user_query["profile"])
    manifest = {
        user_query['user']: manifest_name
    }

    mail_txt(user_query['user'], user_query["body"], user_query["subject"])
    mail_image(user_query['user'], manifest)

if __name__ == "__main__":
    main()
