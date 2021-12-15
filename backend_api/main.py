import resource
import sys

import yt_dlp
import argparse
from shorten import shorten_video


def download_video_srt(videoCode):

    url = "https://www.youtube.com/watch?v=" + videoCode

    ydl_opts = {
        'format': '18',
        'outtmpl': videoCode + '.%(ext)s',
        'subtitlesformat': 'srt',
        'writeautomaticsub': True,
        'subtitleslangs': ['en'],
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        # ydl.download([subs])
        result = ydl.extract_info("{}".format(url), download=True)
        movie_filename = ydl.prepare_filename(result)
    return movie_filename


def memory_limit():
    soft, hard = resource.getrlimit(resource.RLIMIT_AS)
    resource.setrlimit(resource.RLIMIT_AS, (get_memory() * 1024 / 2, hard))

def get_memory():
    with open('/proc/meminfo', 'r') as mem:
        free_memory = 0
        for i in mem:
            sline = i.split()
            if str(sline[0]) in ('MemFree:', 'Buffers:', 'Cached:'):
                free_memory += int(sline[1])
    return free_memory


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument("videoCode", help="give youtube video code")
    args = parser.parse_args()
    print(args.videoCode)

    videoCode = args.videoCode
    download_video_srt(videoCode)

    memory_limit()  # Limitates maximun memory usage to half
    try:
        shorten_video(videoCode)
    except MemoryError:
        sys.stderr.write('nnERROR: Memory Exceptionn')
        sys.exit(1)
