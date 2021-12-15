import yt_dlp

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
        subtitle_info = result.get("requested_subtitles")
        subtitle_language = list(subtitle_info.keys())[0]
        subtitle_ext = subtitle_info.get(subtitle_language).get("ext")
        subtitle_filename = movie_filename.replace(".mp4", ".%s.%s" % (subtitle_language, subtitle_ext))
        subtitle_filename = ""
    return movie_filename, subtitle_filename



if __name__ == '__main__':
    videoCode = "1L6WHxYLacM"
    download_video_srt(videoCode)
    shorten_video(videoCode)