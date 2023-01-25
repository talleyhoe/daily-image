# This file should pull in credentials, setup an email connection, and send
# out our message
# INPUT:
#   user: unique identifier specified in credentials
#       number: who we're texting
#       carrier: cell carrier of the number
#   img-manifest: pair users to images
#       user_id: who do we send this image to
#       image: the image we want to send
# NOTE:
#   There's lots of room for optimization, this is more of a loose framework
#   and is not designed to be used on more than a handful of people

import json, smtplib, ssl, sys
from email.message import EmailMessage

def get_credentials(cred_file = "config/credentials.json") -> dict:
    with open(cred_file, "r") as cred_fp:
        return json.load(cred_fp)

def gen_receiver(number: str, carrier: str) -> str:
    cell_carriers = "config/email-gateways.json"
    with open(cell_carriers, "r") as gateway_fp:
        gateways = json.load(gateway_fp)
    try:
        domain = gateways['mms'][carrier]
        return "@".join((number, domain))
    except Exception as err:
        print("Keyerror: Didn't find carrier match")
        print(err)
        sys.exit(1)

def get_ftype(file_name: str):
    return file_name.split('.')[-1]

def build_message(img: str, msubject: str, 
                  email_to: str, email_from: str) -> EmailMessage:
    msg = EmailMessage()
    msg['From'] = email_from
    msg['To'] = email_to
    msg['Subject'] = msubject

    img_type: str = get_ftype(img)
    with open(img, 'rb') as img_fp:
        img_data = img_fp.read()

    msg.add_attachment(img_data, maintype='image', subtype=img_type)
    return msg

def gen_imgpath(user_id: str, img_manifest: dict, folder = "../images"):
    img_name = img_manifest[user_id]
    return "/".join( (folder, img_name) )

# api calls
def mail_image(user_id: str, img_manifest: dict, 
               subject = "Snowman", images_folder = "images"):
    credentials = get_credentials()
    sender_email = credentials['email']
    sender_smtp = credentials['smtp']
    user = credentials['user'][user_id]
    user_email = gen_receiver(user['number'], user['carrier'])

    imgpath = gen_imgpath(user_id, img_manifest, images_folder)
    msg = build_message(imgpath, subject, user_email, sender_email)

    port = 465  # For SSL
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(sender_smtp, port, context=context) as server:
        server.login(credentials['email'], credentials['pass'])
        server.send_message(msg)
    return 0

def mail_txt(user_id: str, message: str, subject: str):
    credentials = get_credentials()
    sender_email = credentials['email']
    sender_smtp = credentials['smtp']
    user = credentials['user'][user_id]
    user_email = gen_receiver(user['number'], user['carrier'])

    port = 465  # For SSL
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(sender_smtp, port, context=context) as server:
        server.login(credentials['email'], credentials['pass'])
        server.sendmail(sender_email, user_email, message)
    return 0


def test():
    user_id = "talleyhoe"
    img_manifest = { 
        user_id: "test-tux.jpg"
    }
    img_folder = "../test"
    mail_txt(user_id, "Test worked", "Txt test - subject")
    mail_image(user_id, img_manifest, "img test - subject", img_folder)

    return 0

if __name__ == "__main__":
    test()
