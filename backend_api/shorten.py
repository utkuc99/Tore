from moviepy.editor import *
from pyAudioAnalysis import audioBasicIO as aIO
from pyAudioAnalysis import audioSegmentation as aS
import time
import os

def shorten_video(videoCode):

    seconds = time.time()
    local_time = time.ctime(seconds)
    print()
    print("Start time:", local_time)


    # Extract Audio
    clip = VideoFileClip(videoCode + ".mp4")
    if not os.path.isfile(videoCode + ".wav"):
        clip.audio.write_audiofile(videoCode + ".wav")

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
    segments2 = []
    changed = False;
    for i in range(0, len(segments) - 1):
        if (changed == False):
            if ((segments[i + 1][0] - segments[i][1]) < 1.0):
                segment = []
                segment.append(segments[i][0])
                segment.append(segments[i + 1][1])
                segments2.append(segment);
                changed = True
            else:
                segment = []
                segment.append(segments[i][0])
                segment.append(segments[i][1])
                segments2.append(segment);
                changed = False
        else:
            changed = False

    print("Segments with voice : " + str(segments2))

    keep_clips = [clip.subclip(start, end) for [start, end] in segments2]


    edited_video = concatenate_videoclips(keep_clips)
    edited_video.write_videofile(videoCode + "_short.mp4",
                                 preset='ultrafast',
                                 codec='libx264',
                                 temp_audiofile='temp-audio.mp3',
                                 remove_temp=True,
                                 threads=6
                                 )

    """

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
    clip.close()

    seconds2 = time.time()
    local_time = time.ctime(seconds)
    print("End time:", local_time)
    print("Duration:", seconds2 - seconds)

    os.remove(videoCode + ".mp4")
    os.remove(videoCode + ".wav")


    return videoCode + "_short.mp4"
