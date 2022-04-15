from moviepy.editor import VideoFileClip                                # pip install moviepy
from pipeline import pipeline

def processVideo(videopath, resultpath):
    frames = VideoFileClip(videopath)                                   # Read the video
    frames.fl_image(pipeline)                                           # Call the pipeline function
    frames.write_videofile(resultpath, audio=False)                     # Output a resulting video
    frames.reader.close()
    frames.close()

i = 0                                                                   # index of the processed video
videopath = ["project_video.mp4", "challenge_video.mp4", "harder_challenge_video.mp4"]
resultpath = ["result1.mp4", "result2.mp4", "result3.mp4"]
processVideo(videopath[i], resultpath[i])