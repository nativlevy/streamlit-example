import glob
import streamlit as st
import yt_dlp
from moviepy.video.io.VideoFileClip import VideoFileClip
import os

if not os.path.exists('uploaded_files'):
    os.makedirs('uploaded_files')
def save_uploadedfile(uploadedfile):
    with open(os.path.join('uploaded_files', uploadedfile.name), "wb") as f:
        f.write(uploadedfile.getbuffer())
    return st.success("Saved File:{}".format(uploadedfile.name))


url = st.text_input('Video URL')
if "&list" in url:
    url = url.split("&")[0]

start_second = st.text_input('Start minutes:seconds', '0:0')
end_second = st.text_input('End minutes:seconds', '0:00')

minutes, seconds = start_second.split(':')
minutes_end, seconds_end = end_second.split(':')

start_second = int(minutes) * 60 + int(seconds)
end_second = int(minutes_end) * 60 + int(seconds_end)

st.write("Start Second: " + str(start_second), "End Second: " + str(end_second))

ydl_opts = {}

uploaded_file = st.file_uploader("Upload cookies file (for private videos only)")

if uploaded_file:
    st.write(uploaded_file)
    save_uploadedfile(uploaded_file)
    ydl_opts["cookiefile"] = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'uploaded_files',
                                          uploaded_file.name)
    # st.write(ydl_opts["cookiefile"])

if st.button('Convert'):
    # if uploaded_file is not None:
    #     if "_cookies" not in uploaded_file.name:
    #         raise Exception("File name must contain '_cookies'")

    test = os.listdir('.')
    for item in test:
        if item.endswith(".webm") or item.endswith(".mp4") or item.endswith(".mkv") or item.endswith(".mp3"):
            try:
                os.remove(item)
            except:
                pass

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        # st.write(ydl_opts)
        ydl.download(["https://www.youtube.com/watch?v=sEFx0b9y_Xo"])

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
        slides_filename = f"{target_name}_slides.pdf"
        # run(target_name, slides_filename)
        # with open(slides_filename, 'rb') as slides_f:
        #     st.download_button('Download Slides', slides_f, slides_filename)
        try:
            os.remove(filename)
            os.remove(target_name)
            os.remove(uploaded_file.name)
        except:
            pass
        test = os.listdir('.')
        for item in test:
            if item.endswith(".webm") or item.endswith(".mp4") or item.endswith(".mkv") or item.endswith(".mp3"):
                try:
                    os.remove(item)
                except:
                    pass
