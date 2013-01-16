import os
import subprocess
import smtplib
import time
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from RPi import GPIO


def takePicture():
    file = subprocess.check_output('./grabpicture.sh')
    print "picture taken"
    gmailUser = 'email'
    gmailPassword = 'password'
    to = 'destination'

    # Create the container (outer) email message.
    msg = MIMEMultipart()
    msg['Subject'] = 'Spot cannon'
    # me == the sender's email address
    # family = the list of all recipients' email addresses
    msg['From'] = gmailUser
    msg['To'] = to

    # Assume we know that the image files are all in PNG format
    with open(os.path.join('./output/', file.rstrip('\n')), 'rb') as fp:
        img = MIMEImage(fp.read())
        msg.attach(img)

    if not img:
        raise Exception("Failed to generate image")

    # Send the email via our own SMTP server.
    s = smtplib.SMTP('smtp.gmail.com', 587, timeout=20)
    s.ehlo()
    s.starttls()
    s.ehlo()
    s.login(gmailUser, gmailPassword)
    s.sendmail(gmailUser, to, msg.as_string())
    s.quit()
    

def main():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(3, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    while True:
        inputval = GPIO.input(3)
        print inputval
        if not inputval:
            takePicture()
        time.sleep(1)

if __name__ == "__main__":
    main()
