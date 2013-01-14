#!/bin/sh
filename=$(date +"%m-%d-%y|||%H%M%S")
fswebcam -d /dev/video0 ./output/$filename.jpg
echo $filename.jpg
