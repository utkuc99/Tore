from moviepy.editor import *
from pyAudioAnalysis import audioBasicIO as aIO
from pyAudioAnalysis import audioSegmentation as aS
import time
import os
import sys
from google.cloud import videointelligence_v1 as videointelligencepip
import subprocess
from datetime import datetime, timedelta

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'bitirme-345011-8ff740d30042.json'


def checkArray(segments, second):
    for i in segments:
        if(i[0] < second and i[1] > second):
            return 1
    return 0


def shorten_video(videoCode):

    #Take note the start time
    seconds = time.time()
    local_time = time.ctime(seconds)
    print()
    print("Start time:", local_time)

    # Extract Audio
    clip = VideoFileClip(videoCode + ".mp4")
    if not os.path.isfile(videoCode + ".wav"):
        clip.audio.write_audiofile(videoCode + ".wav")

    #Try audio analysis
    try:
        print("trying audio analysis")
        segments = []
        [Fs, x] = aIO.read_audio_file(videoCode + ".wav")
        segments = aS.silence_removal(x, Fs, 0.020, 0.020, smooth_window=1.0, weight=0.1, plot=False)
        #print("Segments with voice : " + str(segments))
    except ValueError:
        print("failed")
        pass
    print("done audio analysis")

    #Calculate segments with audio
    segmentsWithAudio = []
    changed = False;
    for i in range(0, len(segments) - 1):
        if (changed == False):
            if ((segments[i + 1][0] - segments[i][1]) < 1.0):
                segment = []
                segment.append(segments[i][0])
                segment.append(segments[i + 1][1])
                segmentsWithAudio.append(segment);
                changed = True
            else:
                segment = []
                segment.append(segments[i][0])
                segment.append(segments[i][1])
                segmentsWithAudio.append(segment);
                changed = False
        else:
            changed = False
    print("Segments with audio: " + str(segmentsWithAudio))

    # motion scan
    print("trying motion analysis")
    process = subprocess.run("dvr-scan -i " + videoCode + ".mp4 -t 5 -so", stdout=subprocess.PIPE, shell=True)
    output = str(process.stdout)
    x = output.split("values:\\n")[1].split("\\n\'")[0]
    size = len(x)
    y = x.split(",")
    #print(y)
    print("done motion analysis")

    # Calculate segments without motion
    array = []
    for i in range(0, len(y)):
        time2 = datetime.strptime(y[i], '%H:%M:%S.%f')
        a_timedelta = time2 - datetime(1900, 1, 1)
        seconds = a_timedelta.total_seconds()
        array.append(seconds)

    segmentsWithMotion = []
    x = 0
    while x < len(array) - 1:
        segmentsWithMotion.append([array[x], array[x + 1]])
        x = x + 2
    print("Segments with motion: " + str(segmentsWithMotion))

    #Combine Arrays --Work in Progress
    scoreArray = {}
    for i in range(len(clip)):
        secondScore = 0
        secondScore += checkArray(segmentsWithAudio, i)
        secondScore += checkArray(segmentsWithMotion, i)
        scoreArray[i] = secondScore



    #Generate new video
    keep_clips = [clip.subclip(start, end) for [start, end] in segmentsWithAudio]
    edited_video = concatenate_videoclips(keep_clips)
    edited_video.write_videofile("processed_videos/" + videoCode + "_short.mp4",
                                 preset='ultrafast',
                                 codec='libx264',
                                 temp_audiofile='temp-audio.mp3',
                                 remove_temp=True,
                                 threads=6
                                 )

    """
    #Print segments without voice
    otherSegments = []
    for i in range(0, len(segments2) - 1):
        segment = []
        segment.append(segments2[i][1])
        segment.append(segments2[i + 1][0])
        otherSegments.append(segment);

    print("Segments without voice : " + str(otherSegments))

    remove_clips = [clip.subclip(start, end) for [start, end] in otherSegments]

    edited_video2 = concatenate_videoclips(remove_clips)
    edited_video2.write_videofile(videoCode + "_removed.mp4",
                                 preset='ultrafast',
                                 codec='libx264',
                                 temp_audiofile='temp-audio.m4a',
                                 remove_temp=True,
                                 audio_codec="aac",
                                 threads=6
                                 )
    """
    #Close original File
    clip.close()

    #Calculate run time
    seconds2 = time.time()
    local_time = time.ctime(seconds)
    print("End time:", local_time)
    print("Duration:", seconds2 - seconds)

    #Remove unnecesary files
    os.remove(videoCode + ".mp4")
    os.remove(videoCode + ".wav")

    #Return final video
    return videoCode + "_short.mp4"
