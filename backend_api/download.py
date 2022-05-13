import yt_dlp

def download_video(videoCode):

    url = "https://www.youtube.com/watch?v=" + videoCode

    ydl_opts = {
        'format': '18',
        'outtmpl': videoCode + '.%(ext)s',
        'subtitlesformat': 'srt',
        'writeautomaticsub': True,
        #'subtitleslangs': ['en'],
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        # ydl.download([subs])
        result = ydl.extract_info("{}".format(url), download=True)
        movie_filename = ydl.prepare_filename(result)
    return movie_filename
