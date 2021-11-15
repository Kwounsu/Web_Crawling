"""
This program downloads mp3 file from YouTube
- for study purpose only.
- I am using Melon Music
"""

# Crawling
from bs4 import BeautifulSoup
from selenium import webdriver
# Download music
import os.path
from pytube import YouTube


def find_video(url, imp_time=5):
    # Web driver
    driver_loc = '/Users/kwounsulee/PycharmProjects/study/chromedriver'
    driver = webdriver.Chrome(driver_loc)
    driver.implicitly_wait(imp_time)
    driver.get(url)

    # BeautifulSoup
    html = driver.page_source
    bs = BeautifulSoup(html, 'lxml')
    driver.quit()
    os.system("killall -9 'Google Chrome'")

    # get video url
    data = bs.select('a#video-title')
    for x in data:
        x = str(x)
        find = False
        for i in range(len(x)):
            # 2 minutes <= playtime <= 4 minutes
            if not find and x[i:i + 7] == 'minutes' and 2 <= int(x[i - 3:i]) <= 4 and x[i - 6:i - 3] == 'ago':
                find = True
            elif find and x[i:i + 4] == 'href':
                for j in range(i + 6, len(x)):
                    if x[j] == '"':
                        return x[i + 6:j]


print("artist: ", end='')
artist = input().strip()
print("song name: ", end='')
song = input().strip()
file_name = f"{artist} - {song}.mp3"

href = find_video(f'https://www.youtube.com/results?search_query={artist} {song}')
url = 'https://www.youtube.com' + href

YouTube(url).streams.filter(only_audio=True).first().download(filename=file_name)
