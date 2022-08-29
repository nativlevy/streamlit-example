import os

import streamlit as st
import yt_dlp
from moviepy.video.io.VideoFileClip import VideoFileClip

url = st.text_input('Video URL')

# url = "https://www.youtube.com/clip/UgkxgdZs6VsmysTGCzZQvpIvVM2IM4H-aJ9w"
# url = "https://www.youtube.com/clip/UgkxSBQ7LQeHv-pJezfqT4ZEEa7HWeemcq_V"

start_second = st.text_input('Start second')
end_second = st.text_input('End second')

start_second = int(start_second) if start_second else 0
end_second = int(end_second) if end_second else 0

if st.button('Convert'):
    filename = 'video.mkv'

    # try:
    #     open(filename, 'w').close()
    # except Exception:
    #     pass

    ydl_opts = {'outtmpl': filename, '--no-continue': True}  # 'f': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/mp4'}

    # if the file exists, delete it
    if os.path.exists(filename):
        os.remove(filename)

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

    target_name = 'part.mp4'

    with VideoFileClip(filename) as video:
        new = video.subclip(start_second, end_second)
        new.write_videofile(target_name, audio_codec='aac')

    with open(target_name, 'rb') as f:
        st.download_button('Download Video', f, target_name)
        # os.remove(filename)
        # os.remove(target_name)
