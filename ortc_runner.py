import ortc
import time
import json
import datetime
import os
import subprocess
import RPi.GPIO as GPIO

ortc_client = ortc.OrtcClient() 

channel = 'bank'

def on_connected(sender):
    print 'Connected to Realtime.co'
    ortc_client.subscribe(channel, True, on_message)
 
def on_message(sender, channel, message):
    raw_time = datetime.datetime.now()
    formatted_time = raw_time.strftime("%I:%M:%S %p")
    
    parsed_json = json.loads(message)
    
    if parsed_json['text'] == 'PING' :
        message = '{"id":"ID_DEV1","text":"PONG, IM ALIVE","sentAt":"' + formatted_time + '"}'
        ortc_client.send(channel, message)

    if parsed_json['text'] == 'BRI' :
        data = 123456
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(17,GPIO.OUT)
        GPIO.output(17, 1)
        time.sleep(1)
        GPIO.output(17, 0)

        activate_webcam = subprocess.call('fswebcam --no-banner -r 1920x1080 --crop 480x155,570x500 image.jpg', shell=True)

        get_data = os.popen('ssocr -t 30 image.jpg -D -d -1').read()

        upload_s3 = os.system('sh upload_s3.sh')


        

        data = get_data.rstrip('\n')

        data.translate(None, "_-,.")

        
        print data
        message = '{"id":"ID_DEV1","text":"'+ str(data) +'","sentAt":"' + formatted_time + '"}'
        ortc_client.send(channel, message)
 
def on_subscribed(sender, channel):
    raw_time = datetime.datetime.now()
    formatted_time = raw_time.strftime("%I:%M:%S %p")

    print 'Subscribed to channel : ' + channel
    message = '{"id":"ID_DEV1","text":"HI, IM ALIVE :)","sentAt":"' + formatted_time + '"}'
    ortc_client.send(channel, message)
 
ortc_client.set_on_connected_callback(on_connected)
ortc_client.set_on_subscribed_callback(on_subscribed)

ortc_client.cluster_url = "http://ortc-developers.realtime.co/server/2.1"
ortc_client.connect('BGmLm4')


try:
    while True:

        time.sleep(1)
except:
     pass