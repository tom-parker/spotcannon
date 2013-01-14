import os
import subprocess
import smtplib
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart

import time
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
    fp = open(os.path.join('./output/', file.rstrip('\n')), 'rb')
    img = MIMEImage(fp.read())
    fp.close()
    msg.attach(img)

    # Send the email via our own SMTP server.
    s = smtplib.SMTP('smtp.gmail.com', 587, timeout=20)
    s.ehlo()
    s.starttls()
    s.ehlo()
    s.login(gmailUser, gmailPassword)
    s.sendmail(gmailUser, to, msg.as_string())
    s.quit()

GPIO.setmode(GPIO.BOARD)
GPIO.setup(3, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
while True:
    inputval = GPIO.input(3)
    print inputval
    if(inputval == False):
        takePicture()
    time.sleep(1)
