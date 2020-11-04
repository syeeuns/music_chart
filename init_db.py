import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

client = MongoClient('localhost', 27017)
db = client.dbmusic

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}

url = 'https://www.melon.com/chart/index.htm'
data = requests.get(url, headers=headers)
soup = BeautifulSoup(data.text, 'html.parser')
target = soup.select('#frm > div > table > tbody > tr')

db.musics.drop()

for one in target:
    img = one.select_one('td:nth-child(2) > div > a > img')['src']
    title = one.select_one('td:nth-child(4) > div > div > div.ellipsis.rank01 > span > a').text
    artist = one.select_one('td:nth-child(4) > div > div > div.ellipsis.rank02 > a').text
    album = one.select_one('td:nth-child(2) > div > a > img')['alt'].split('-')[0]
    music = {
        'img':img,
        'title':title,
        'artist':artist,
        'album':album,
        'like': 0
    }

    db.musics.insert_one(music)