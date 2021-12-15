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



if __name__ == '__main__':


    parser = argparse.ArgumentParser()
    parser.add_argument("videoCode", help="give youtube video code")
    args = parser.parse_args()
    print(args.videoCode)

    videoCode = args.videoCode
    download_video_srt(videoCode)
    shorten_video(videoCode)