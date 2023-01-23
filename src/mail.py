# This file should pull in credentials, setup an email connection, and send
# out our message

import json, smtplib, ssl

def main():
    port = 465  # For SSL
    password = input("Type your password and press enter: ")

    # Create a secure SSL context
    context = ssl.create_default_context()

    with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
        server.login("my@gmail.com", password)
        # TODO: Send email here

if __name__ == "__main__":
    main()
