from moviepy.editor import *
import time
import os
from audioAnalysis import audio_analysis
from motionAnalysis import motion_analysis
from subtitleAnalysis import subtitle_analysis


def checkArray(segments, second):
    for i in segments:
        if i[0] < second < i[1]:
            return 1
    return 0


def shorten_video(videoCode):
    clip = VideoFileClip(videoCode + ".mp4")

    # Take note the start time
    seconds = time.time()
    local_time = time.ctime(seconds)
    print()
    print("Start time:", local_time)

    # Try audio analysis
    segmentsWithAudio = audio_analysis(videoCode)

    # Try motion analysis
    segmentsWithMotion = motion_analysis(videoCode)

    # Try subtitle analysis
    segmentsWithSubtitle = subtitle_analysis(videoCode)

    # Combine Arrays
    scoreArray = []
    for i in range(int(clip.duration)):
        secondScore = 0
        secondScore += checkArray(segmentsWithAudio, i)
        secondScore += checkArray(segmentsWithMotion, i)
        secondScore += checkArray(segmentsWithSubtitle, i)
        scoreArray.append(secondScore)
    print("Score Array:" + str(scoreArray))

    finalArray = []
    activeSegm = False
    segment = []
    for i in range(len(scoreArray)):
        if activeSegm:
            if scoreArray[i] != 2:
                segment.append(i-1)
                finalArray.append(segment)
                segment = []
                activeSegm = False
        else:
            if scoreArray[i] == 2:
                segment.append(i)
                activeSegm = True

    print("Final segments: " + str(finalArray))


    # Generate new video
    keep_clips = [clip.subclip(start, end) for [start, end] in finalArray]
    edited_video = concatenate_videoclips(keep_clips)
    edited_video.write_videofile("processed_videos/" + videoCode + "_short.mp4",
                                 preset='ultrafast',
                                 codec='libx264',
                                 temp_audiofile='temp-audio.mp3',
                                 remove_temp=True,
                                 threads=6
                                 )

    # Close original File
    clip.close()

    # Calculate run time
    seconds2 = time.time()
    local_time = time.ctime(seconds)
    print("End time:", local_time)
    print("Duration:", seconds2 - seconds)

    # Remove unnecesary files
    #os.remove(videoCode + ".mp4")
    os.remove(videoCode + ".wav")

    return videoCode + "_short.mp4"
