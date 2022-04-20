#!usr/bin/python
from moviepy.editor import VideoFileClip                                # pip install moviepy
from pipeline import pipeline
import sys

def processVideo(videopath, resultpath, debug_mode_on):
    frames = VideoFileClip(videopath)  # Read the video
    myframes = frames.fl_image(lambda image: pipeline(image, debug_mode_on))
    myframes.write_videofile(resultpath, audio=False)  # Output a resulting video
    frames.reader.close()
    frames.close()


n = len(sys.argv)
if n < 2:
    print("Error: Please pass the video path as an argument")
    sys.exit(0)
videopath = sys.argv[1]
if n > 2:
    resultpath = "./"+sys.argv[2]
else:
    resultpath = "./result.mp4"
# Getting the mode 0 means normal (default), 1 means debug
if n > 3:
    debug_mode_on = sys.argv[3]
else:
    debug_mode_on = 0

processVideo(videopath, resultpath, debug_mode_on)
