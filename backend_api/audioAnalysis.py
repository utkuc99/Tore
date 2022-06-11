# Try audio analysis

from moviepy.editor import *
from pyAudioAnalysis import audioBasicIO as aIO
from pyAudioAnalysis import audioSegmentation as aS


def audio_analysis(videoCode):
    # Extract Audio
    clip = VideoFileClip(videoCode + ".mp4")
    if not os.path.isfile(videoCode + ".wav"):
        clip.audio.write_audiofile(videoCode + ".wav")
    if not os.path.isfile(videoCode + ".mp3"):
        clip.audio.write_audiofile(videoCode + ".mp3")

    try:
        print("trying audio analysis")
        segments = []
        [Fs, x] = aIO.read_audio_file(videoCode + ".wav")
        segments = aS.silence_removal(x, Fs, 0.020, 0.020, smooth_window=1.0, weight=0.1, plot=False)
        # print("Segments with voice : " + str(segments))
    except ValueError:
        print("failed")
        pass
    print("done audio analysis")

    # Calculate segments with audio
    segmentsWithAudio = []
    changed = False;
    for i in range(0, len(segments) - 1):
        if not changed:
            if (segments[i + 1][0] - segments[i][1]) < 1.0:
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
    return segmentsWithAudio
