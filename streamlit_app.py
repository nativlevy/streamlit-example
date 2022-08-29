import streamlit as st
import yt_dlp

st.write("# Download Video")
url = st.text_input('The video URL (youtube)')

if st.button('Convert'):
    filename = 'video'
    ydl_opts = {'outtmpl': filename}  # 'f': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]'}
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

    with open(filename + '.mkv', 'rb') as f:
        st.download_button('Download Video', f, 'video.mkv')

