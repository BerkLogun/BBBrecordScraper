import requests
import os
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from moviepy.editor import *
import time


def url_fetcher():
    url = input('Enter the record url: ')
    driver = webdriver.Chrome('./chromedriver')
    driver.get(url)

    time.sleep(5)

    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')

    all_videos = soup.findAll('video')
    video_name = soup.find('span', class_="title interactive").text
    video_name = video_name.replace(' ', '_')
    video_name = video_name.replace(':', '_')
    video_name = video_name.replace('?', '_')
    video_name = video_name.replace('/', '_')
    video_name = video_name.replace('\\', '_')
    video_name = video_name.replace('*', '_')
    video_name = video_name.replace('<', '_')
    video_name = video_name.replace('>', '_')
    video_name = video_name.replace('|', '_')
    video_name = video_name.replace('"', '_')

    video_name = '__'+video_name + '.mp4'



    sources = []


    for video in all_videos:
        #print(video['src'])
        sources.append(video['src'])


    webcam_url = 'https://scalelite.deu.edu.tr' + sources[0]
    deskshare_url = 'https://scalelite.deu.edu.tr' + sources[1]

    return webcam_url, deskshare_url, video_name



def download_video(url, filename):
    r = requests.get(url, stream=True)
    print('Downloading video... '+filename)

    with open(filename, 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)
        f.close()




if __name__ == '__main__':
    webcam_url, deskshare_url, video_name = url_fetcher()
    download_video(webcam_url, 'webcam'+video_name)
    download_video(deskshare_url, 'deskshare'+video_name)

    webcam_clip = VideoFileClip('webcam'+video_name)
    deskshare_clip = VideoFileClip('deskshare'+video_name)
    webcam_audio = webcam_clip.audio

    audio_clip = CompositeAudioClip([webcam_audio])
    deskshare_clip.audio = audio_clip
    deskshare_clip.write_videofile(video_name)

    webcam_clip.close()
    deskshare_clip.close()

    time.sleep(5)

    os.remove('webcam'+video_name)
    os.remove('deskshare'+video_name)
