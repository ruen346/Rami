import requests
import json
from Recorder import record_audio, read_audio

from gtts import gTTS
import pygame

from urllib.request import urlopen, Request
import urllib
import bs4
import os
from bs4 import BeautifulSoup
from googletrans import Translator
import time

import speech_recognition as sr

# Wit speech API endpoint
API_ENDPOINT = 'https://api.wit.ai/speech'

# Wit.ai api access token
wit_access_token = 'Y4IHSD5VB7NBUKCOM6AZ7KSBTSYO3ZDY'


def RecognizeSpeech(AUDIO_FILENAME, num_seconds=5):
    # record audio of specified length in specified audio file
    record_audio(num_seconds, AUDIO_FILENAME)

    # reading audio
    audio = read_audio(AUDIO_FILENAME)

    # defining headers for HTTP request
    headers = {'authorization': 'Bearer ' + wit_access_token,'Content-Type': 'audio/wav'}

    # making an HTTP post request
    resp = requests.post(API_ENDPOINT, headers=headers,data=audio)

    # converting response content to JSON format
    data = json.loads(resp.content)

    # get text from data
    text = data['text']

    # return the text
    return text


if __name__ == "__main__":
    text = RecognizeSpeech('myspeech.wav', 4)
    print("\nYou said: {}".format(text))












i = 0  # 저장 count
active = 1  # 활성화시 1
rest = 0  # 휴먼모드에 진입할때 1 진입하자마자 0
word_go_active = 0  # 끝말잇기 게임시 1


def weather(question):
    i = question.find('날씨')
    question = question[:i - 1]
    i = question.rfind(' ')
    location = question[i + 1:]

    counts = 0
    if question.find('내일') != -1:
        counts = 1
    elif question.find('모래') != -1:
        counts = 2
    else:
        counts = 0

    global text

    enc_location = urllib.parse.quote(location + '+날씨')
    url = "https://search.naver.com/search.naver?ie=utf8&query=" + enc_location
    user_agent = 'Mozilla/5.0'
    headers = {'referer': 'http://naver.com', 'User-Agent': user_agent}
    req = Request(url, headers=headers)
    html = urlopen(req).read()
    soup = bs4.BeautifulSoup(html, "html.parser")

    if counts == 0:
        text = '현재 ' + location + ' 날씨는 ' + soup.find('ul', class_='info_list').find('p',
                                                                                         class_='cast_txt').text + '. 온도는 ' + soup.find(
            'p', class_='info_temperature').find('span', class_='todaytemp').text + '도 입니다.'
    elif counts == 1:
        for texts in soup.find_all('div', class_='tomorrow_area _mainTabContent'):
            texts2 = texts.find_all('span', class_='todaytemp')
            texts3 = texts.find_all('p', class_='cast_txt')
        text = '내일 오전 날씨는 ' + texts3[0].text + "이고 온도는 " + texts2[0].text + "도 입니다. 오후 날씨는 " + texts3[1].text + "이고 온도는 " + texts2[1].text + "도 입니다."
    elif counts == 2:
        for texts in soup.find_all('div', class_='tomorrow_area'):
            texts2 = texts.find_all('span', class_='todaytemp')
            texts3 = texts.find_all('p', class_='cast_txt')
        text = '모래 오전 날씨는 ' + texts3[0].text + "이고 온도는 " + texts2[0].text + "도 입니다. 오후 날씨는 " + texts3[1].text + "이고 온도는 " + texts2[1].text + "도 입니다."


def such(question):
    i = question.find('뭐야')
    if i == -1:
        i = question.find('누구야')
    question = question[:i - 2]

    enc_qu = urllib.parse.quote(question)
    url = "https://ko.wikipedia.org/wiki/" + enc_qu
    user_agent = 'Mozilla/5.0'
    headers = {'referer': 'http://naver.com', 'User-Agent': user_agent}
    req = Request(url, headers=headers)
    html = urlopen(req).read()
    soup = bs4.BeautifulSoup(html, "html.parser")
    global text
    text = question + '란 ' + soup.find('div', class_='mw-parser-output').find('p').text


def naver_such(question):
    i = question.find('기사')
    question = question[:i - 1]

    enc_qu = urllib.parse.quote(question)
    url = "https://search.naver.com/search.naver?where=news&sm=tab_jum&query=" + enc_qu
    user_agent = 'Mozilla/5.0'
    headers = {'referer': 'http://naver.com', 'User-Agent': user_agent}
    req = Request(url, headers=headers)
    html = urlopen(req).read()
    soup = bs4.BeautifulSoup(html, "html.parser")
    global text
    text = soup.find('ul', class_='type01').find('dt').text


def word_go(question):
    question = question[-1]
    question += '로 시작하는 단어'

    enc_qu = urllib.parse.quote(question)
    url = "https://dict.naver.com/search.nhn?query=" + enc_qu
    print(url)
    user_agent = 'Mozilla/5.0'
    headers = {'referer': 'http://naver.com', 'User-Agent': user_agent}
    req = Request(url, headers=headers)
    html = urlopen(req).read()
    soup = bs4.BeautifulSoup(html, "html.parser")
    global text
    text = soup.find('ul', class_='lst_krdic').find('span', class_='c_b').text


def now_such(question):
    global text
    url = "http://naver.com"
    user_agent = 'Mozilla/5.0'
    headers = {'referer': 'http://naver.com', 'User-Agent': user_agent}
    req = Request(url, headers=headers)
    html = urlopen(req).read()
    soup = BeautifulSoup(html, "html.parser")
    global text
    text = ' '
    for idx, tag in enumerate(soup.select('.PM_CL_realtimeKeyword_rolling .ah_item .ah_k'), 1):
        texts = (idx, tag.text)
        text += str(texts[0]) + '위 ' + str(texts[1]) + ' '


def times():
    global text
    t = time.localtime()
    text = str(t.tm_mon) + '월 ' + str(t.tm_mday) + '일 ' + str(t.tm_hour) + '시 ' + str(t.tm_min) + '분 입니다'


def trance_word(question):
    i = question.find('번역')
    question = question[:i - 1]
    global text
    translator = Translator()
    translations = translator.translate(question, dest='en')
    text = translations.text

a = 1
if a==1:
    question = text # 질문 로그

    # 처리 데이터베이스
    if word_go_active == 1:  # 0순위
        if question.find('종료') == -1:
            word_go(question)
        else:
            text = '끝말잇기를 종료합니다'
            word_go_active = 0
    elif question == '라미':  # 1순위
        text = '네 무엇을 도와드릴까요'
        active = 1
    elif active == 0:
        active = 0
    elif (question.find('라미') != -1) & (question.find('쉬어') != -1):
        text = '휴먼모드에 진입합니다'
        rest = 1
    elif (question.find('뭐야') != -1) | (question.find('누구야') != -1):  # 2순위
        such(question)
    elif question.find('기사') != -1:
        naver_such(question)
    elif question.find('번역') != -1:
        trance_word(question)
    elif question.find('날씨') != -1:  # 3순위
        weather(question)
    elif question.find('실시간 검색 순위') != -1:  # 4순위
        now_such(question)
    elif question.find('몇시') != -1:
        times()
    elif question.find('끝말잇기') != -1:
        word_go_active = 1
        text = '먼저 시작하세요'
    elif question == '안녕':  # 5순위
        text = '안녕하세요'
    elif (question.find('뭐라고') != -1) | (question.find('다시 말해봐') != -1):
        text = text
    elif question.find('종료') != -1:
        pygame.mixer.quit()
    else:
        text = question

    if active == 1:
        print("답변 : " + text)  # 출력 로그






    tts = gTTS(text=text, lang='ko')
    sound = "sound.mp3"
    tts.save(sound)
    read_audio('sound.mp3')

    # 음성설정
    freq = 24000  # sampling rate, 44100(CD), 16000(Naver TTS), 24000(google TTS)
    bitsize = -16  # signed 16 bit. support 8,-8,16,-16
    channels = 1  # 1 is mono, 2 is stereo
    buffer = 2048  # number of samples (experiment to get right sound)

    # 음성 호출
    pygame.mixer.init(freq, bitsize, channels, buffer)
    pygame.mixer.music.load(sound)
    pygame.mixer.music.play(0)
    clock = pygame.time.Clock()
    while pygame.mixer.music.get_busy():
        clock.tick(30)
    pygame.mixer.quit()

