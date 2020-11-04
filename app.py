import requests
from bs4 import BeautifulSoup
from pymongo import MongoClient
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

client = MongoClient('localhost', 27017)
db = client.dbmusic

@app.route('/')
def home():
    return render_template('index.html')


@app.route('/list', methods=['GET'])
def show():
    result = list(db.musics.find({},{'_id':0}))
    return jsonify({'result':'success', 'chart':result})


@app.route('/like', methods=['POST'])
def like():
    title = request.form['title']
    result = db.musics.find_one({'title':title}, {'_id': 0})
    new_like = result['like'] + 1
    db.musics.update_one({'title':title}, {'$set':{'like':new_like}})
    return jsonify({'result':'success', 'msg':title +' : 좋아요 완료!'})


@app.route('/del', methods=['POST'])
def delete():
    title = request.form['title']
    db.musics.delete_one({'title': title})
    return jsonify({'result': 'success', 'msg': title + ' : 삭제 완료!'})


if __name__ == '__main__':
    app.run()