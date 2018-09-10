#!/bin/bash

gpio -g mode 17 out
gpio -g write 17 1
sleep 1
gpio -g write 17 0
fswebcam --no-banner -r 1920x1080 --crop 500x155,550x500 image.jpg



#!fswebcam -r 1920x1080 --no-banner /var/www/html/image.jpg
