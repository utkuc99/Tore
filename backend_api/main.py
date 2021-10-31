import argparse
import youtube_dl
import moviepy.editor as mp


def download_video_srt(subs):
    """ Downloads specified Youtube video's subtitles as a vtt/srt file.
    Args:
        subs(str): Full url of Youtube video
    Returns:
        True
    The video will be downloaded as 1.mp4 and its subtitles as 1.(lang).srt
    Both, the video and its subtitles, will be downloaded to the same location
    as that of this script (sum.py)
    """
    ydl_opts = {
        'format': 'best',
        'outtmpl': 'video.%(ext)s',
        'subtitlesformat': 'srt',
        'writeautomaticsub': True,
        'subtitleslangs': ['tr'],
    }

    movie_filename = ""
    subtitle_filename = ""
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        # ydl.download([subs])
        result = ydl.extract_info("{}".format(url), download=True)
        movie_filename = ydl.prepare_filename(result)
        subtitle_info = result.get("requested_subtitles")
        subtitle_language = list(subtitle_info.keys())[0]
        subtitle_ext = subtitle_info.get(subtitle_language).get("ext")
        subtitle_filename = movie_filename.replace(".mp4", ".%s.%s" %(subtitle_language, subtitle_ext))
    return movie_filename, subtitle_filename


if __name__ == '__main__':
    parser = argparse.ArgumentParser("Watch videos quickly")
    parser.add_argument('-u', '--url', help="Video url", type=str)

    args = parser.parse_args()

    url = "https://www.youtube.com/watch?v=JBaYiSyH3CY"

    # download video with subtitles
    movie_filename, subtitle_filename = download_video_srt(url)

    #Extract Audio
    my_clip = mp.VideoFileClip("video.mp4")
    my_clip.audio.write_audiofile("audio.mp3")