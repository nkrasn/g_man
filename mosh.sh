#!/bin/bash
#./ffmpeg4-2-2/ffmpeg -i ./vids/mosh/target.mp4 ./vids/mosh/target.avi
# ARG1: filename in ./vids/mosh
# ARG2: avi quality
# ARG3: size (WIDTHxHEIGHT)
#./ffmpeg4-2-2/ffmpeg -i ./vids/mosh/$1 -s $3 -g $2 ./vids/mosh/target.avi
#   set -e # exit if any line fails
#   echo "EXECUTING first"
#ffmpeg4-2-2/ffmpeg -y -i $1 -s $3 -g $2 vids/targetmosh.avi
#./ffmpeg4-2-2/ffmpeg -i ./vids/mosh/$1 ./vids/mosh/target.avi
#   echo "EXECUTING second"
#   datamosh vids/targetmosh.avi -o vids/outmosh.avi
#   echo "EXECUTING third"
#   ffmpeg -y -i vids/outmosh.avi vids/out.mp4
#rm vids/targetmosh.avi
#rm vids/outmosh.avi




set -e # exit if any line fails
ffmpeg4-2-2/ffmpeg -y -i $1 -g $2 -vf scale=$3:-2 vids/targetmosh.avi
datamosh vids/targetmosh.avi -o vids/outmosh.avi
ffmpeg4-2-2/ffmpeg -y -i vids/outmosh.avi -fs 7M vids/out.mp4

