# PiCam
A python code that uses the Raspberry Pi to make a photo booth

Run the following commands in the terminal:

`sudo apt-get update`

`sudo apt-get upgrade`


`git clone https://github.com/sampdubs/PiCam.git`

`cd PiCam/`


`pip3 install tweepy`

`pip3 install picamera`


`mkdir images`

`touch passwords.txt`

`nano passwords.txt`

Enter your email password

`ctrl-x y enter`

* Sign up for a Twitter developer account [here](https://dev.twitter.com)

* Make a new app and find the api key, api secret, access token, and access token secret

* Connect a buzzer to pin 3

* Connect a button to pin 4

* Plug a camera module into the camera port (blue side facing the ethernet port)

* Edit picam.py so that you use your own email adress and Twitter information

`python3 picam.py`
