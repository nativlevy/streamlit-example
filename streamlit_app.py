import os
import glob

import streamlit as st
import yt_dlp
from moviepy.video.io.VideoFileClip import VideoFileClip
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip

url = st.text_input('Video URL')
if "&list" in url:
    url = url.split("&")[0]

start_second = st.text_input('Start minutes:seconds', '0:0')
end_second = st.text_input('End minutes:seconds', '0:0')

minutes, seconds = start_second.split(':')
minutes_end, seconds_end = end_second.split(':')

start_second = int(minutes) * 60 + int(seconds)
end_second = int(minutes_end) * 60 + int(seconds_end)

st.write("Start Second: " + str(start_second), "End Second: " + str(end_second))

if st.button('Convert'):
    test = os.listdir('.')
    for item in test:
        if item.endswith(".webm") or item.endswith(".mp4") or item.endswith(".mkv") or item.endswith(".mp3"):
            try:
                os.remove(item)
            except:
                pass

    ydl_opts = {}

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

    list_of_files = glob.glob('*')  # * means all if need specific format then *.csv
    filename = max(list_of_files, key=os.path.getctime)
    print(filename)

    target_name = 'part.mp4'

    with VideoFileClip(filename) as video:
        new = video.subclip(start_second, end_second)
        new.write_videofile(target_name, audio_codec='aac')
#         ffmpeg_extract_subclip(filename, start_second, end_second, targetname=target_name)

    with open(target_name, 'rb') as f:
        st.download_button('Download Video', f, target_name)
        try:
            os.remove(filename)
            os.remove(target_name)
        except:
            pass
        test = os.listdir('.')
        for item in test:
            if item.endswith(".webm") or item.endswith(".mp4") or item.endswith(".mkv") or item.endswith(".mp3"):
                try:
                    os.remove(item)
                except:
                    pass
