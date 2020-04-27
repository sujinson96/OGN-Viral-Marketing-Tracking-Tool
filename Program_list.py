from flask import Flask, render_template, jsonify, request
app = Flask(__name__)

import requests
from bs4 import BeautifulSoup

from pymongo import MongoClient
client = MongoClient('localhost', 27017)
db = client.dbsparta

@app.route('/programlist')
def home1():
   return render_template('등록페이지.html')

@app.route('/programlist', methods=['POST'])
def saving():
   # 1. 클라이언트로부터 데이터를 받기
   programtitle_receive = request.form['programtitle_give']
   programkeyword_receive = request.form['programkeyword_give']

   program_title = {
      'programs': programtitle_receive,
      'keywords' : programkeyword_receive
   }

   db.programlist.insert_one(program_title)

   return jsonify({'result': 'success'})

@app.route('/dropmenu', methods=['GET'])
def listing():

    result = list(db.programlist.find({}, {'_id' : 0}))
    return jsonify({'result':'success', 'program_title': result})

@app.route('/dropmenu', methods=['POST'])
def addkeyword():
   # 1. 클라이언트로부터 데이터를 받기
   dropmenutitle_receive = request.form['dropmenutitle_give']
   dropmenukeyword_receive = request.form['dropmenukeyword_give']

   old_program = db.programlist.find_one({'programs': dropmenutitle_receive})
   old_keyword = old_program['keywords']
   new_keywords = old_keyword + ', ' + dropmenukeyword_receive
   db.programlist.update_one({'programs': dropmenutitle_receive}, {'$set': {'keywords' : new_keywords}})

   return jsonify({'result': 'success'})

@app.route('/program_table', methods=['GET'])
def make_table():

    result = list(db.programlist.find({}, {'_id' : 0}))
    return jsonify({'result':'success', 'program_title': result})

@app.route('/community_viral')
def home2():
   return render_template('조회페이지.html')

@app.route('/viral_menu', methods=['GET'])
def community_viral_menu():

    result = list(db.programlist.find({}, {'_id' : 0}))
    return jsonify({'result':'success', 'program_title': result})

@app.route('/keyword_table', methods=['GET'])
def keyword_table():
    title_receive = request.args.get('program_title_give')
    result = list(db.community_data.find({'program': title_receive}, {'_id' : 0}))
    return jsonify({'result':'success', 'community_data': result})


@app.route('/delete', methods=['POST'])
def posttitle():
   # 1. 클라이언트로부터 데이터를 받기
   posturl_receive = request.form['posturl_give']

   db.programlist.update_one({'programs': posturl_receive}, {'$set': {'property' : False}})

   return jsonify({'result': 'success'})


if __name__ == '__main__':
   app.run('0.0.0.0', port=5001, debug=True)


