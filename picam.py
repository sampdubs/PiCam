from os import system
system('clear')
print('Just a sec...')
import tweepy
from email.message import EmailMessage
import imghdr
import smtplib as email
from picamera import PiCamera
from gpiozero import Button, Buzzer
from time import sleep
import json
print('Done :)')
sleep(0.75)
system('clear')

button = Button(4)
buzz = Buzzer(3)
buzz.off()
cam = PiCamera()
TWITTER = 1
EMAIL = 2
BOTH = 3
CONFIG = json.loads(open('config.json').read())

def main():
    system('clear')
    
    onTwitter = ' '
    handle = ''
    burst = ' '
    postOn = ''
    while postOn not in ['1', '2', '3']:
        postOn = input('Would you like your images posted on Twitter [1], sent to you in an email [2], or both [3] (enter a number)? ')
    postOn = int(postOn)
    if postOn == TWITTER or postOn == BOTH:
        while onTwitter[0].lower() != 'y' and onTwitter[0].lower() != 'n':
            onTwitter = input('Do you have a Twitter account? [y/n] ') + ' '
        onTwitter = onTwitter[0].lower() == 'y'
        if onTwitter:
            handle = '@' + input('What is your Twitter handle? ')
        else:
            handle = input('What is your name? ')
    eobj = None
    msg = None
    recipients = ','
    if postOn == EMAIL or postOn == BOTH:
        eobj = email.SMTP('smtp.gmail.com', 587)
        pwd = open('passwords.txt').read()
        eobj.ehlo()
        eobj.starttls()
        eobj.login(CONFIG['email'], pwd)
        while '@' not in recipients or ',' in recipients:
            recipients = input('Please enter the email adress(es) that you would like the pictures to be sent to (separated by spaces, no commas): ')
        recipients = ', '.join(recipients.split())
        msg = EmailMessage()
        msg['Subject'] = 'Your PiCam pics'
        msg['From'] = 'picam@coolstuff.com'
        msg['To'] = recipients
        msg.set_content('Your really great pictures taken from and sent by a Raspberry Pi!')
        
    while burst[0].lower() != 'y' and burst[0].lower() != 'n':
        burst = input('Would you like to take a burst (alternative is 3 seconds in between pictures to change pose)? [y/n] ')
    burst = burst[0].lower() == 'y'

    imgnum = None
    while imgnum not in ['1', '2', '3', '4']:
        imgnum = input('How many pictures would you like to take (min 1, max 4)? ')
    imgnum = int(imgnum)
    
    if burst:
        print('The camera will count down from 3, then take {} pictures'.format(imgnum))
    else:
        print('The camera will count down from 3, then take a picture and do that {} times'.format(imgnum))

    sleep(1.5)
    input('Press enter when you are ready. ')

    cam.start_preview()

    if burst:
        for i in [3, 2, 1]:
            cam.annotate_text = str(i)
            buzz.on()
            sleep(0.5)
            buzz.off()
            sleep(0.5)
        for i in range(imgnum):
            cam.annotate_text = 'Smile!!'
            sleep(0.2)
            cam.annotate_text = ''
            cam.capture('images/image{}.jpg'.format(i))
    else:
        for i in range(imgnum):
            for j in [3, 2, 1]:
                cam.annotate_text = str(j)
                buzz.on()
                sleep(0.5)
                buzz.off()
                sleep(0.5)
            cam.annotate_text = 'Smile!!'
            sleep(0.75)
            cam.annotate_text = ''
            cam.capture('images/image{}.jpg'.format(i))

    cam.stop_preview()
    
    system('clear')
    if postOn == EMAIL or postOn == BOTH:
        print('Please be patient as your files are emailed to you.')
        filenames = ['images/image{}.jpg'.format(i) for i in range(imgnum)]
        for file in filenames:
            img_data = open(file, 'rb').read()
            msg.add_attachment(img_data, maintype='image', subtype=imghdr.what(None, img_data))
        eobj.send_message(msg)
        system('clear')
    if postOn == TWITTER or postOn == BOTH:
        print('Please be patient while your photos are uploaded to Twitter')
        
        api_key, api_secret, access_token, access_token_secret = CONFIG['api_key'], CONFIG['api_secret'], CONFIG['access_token'], CONFIG['access_token_secret']

        auth = tweepy.OAuthHandler(api_key, api_secret)
        auth.set_access_token(access_token, access_token_secret)

        api = tweepy.API(auth)

        filenames = ['images/image{}.jpg'.format(i) for i in range(imgnum)]
        media_ids = []
        for file in filenames:
            media_ids.append(api.media_upload(file).media_id)

        api.update_status(status='Photos from {}\'s PiCam taken by {}! #PiCamp'.format(CONFIG['name'], handle), media_ids=media_ids)
        cdown = list(range(11))
        cdown.reverse()
        for i in cdown:
            system('clear')
            print('Hold control and click this link in the next {} seconds to see your pics:\nhttps://twitter.com/{}'.format(i, CONFIG['twitter_handle']))
            sleep(1)

while True:
    system('clear')
    print('Press the button to start')
    button.wait_for_press()
    main()

