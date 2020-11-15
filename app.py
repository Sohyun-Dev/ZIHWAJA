from flask import Flask, render_template, jsonify, request
from pymongo import MongoClient  # pymongo를 임포트 하기(패키지 인스톨 먼저 해야겠죠?)
import requests

app = Flask(__name__)

client = MongoClient('mongodb://test:test@52.78.187.20', 27017)  # mongoDB는 27017 포트로 돌아갑니다.
db = client.zihwaja  # 'zihwaja'라는 이름의 db를 만듭니다.


## HTML을 주는 부분
@app.route('/')
def home():
    return render_template('index.html')


## API 역할을 하는 부분
@app.route('/stations/<line>', methods=['GET'])
def read_stations(line):
    # print(line)
    stations = list(db.seoul_subway.find({}, {'_id': 0}))
    # print(stations)
    return jsonify({'result': 'success', 'stations': stations})


@app.route('/stations/<selectedLine>/<selectedStation>', methods=['GET'])
def test(selectedLine, selectedStation):
    station = list(
        db.seoul_subway.find(
            {"LN_NM": selectedLine, "STIN_NM": selectedStation},
            {'_id': 0}
        )
    )

    op_code = str(station[0]['RAIL_OPR_ISTT_CD'])
    line_code = str(station[0]['LN_CD'])
    station_code = str(station[0]['STIN_CD'])
    response = requests.get(url)
    result_cnt = response.json()['header']['resultCnt']

    result_list = []
    if result_cnt != 0:
        result_list = response.json()['body']

    return jsonify({'result': 'success', 'stations': result_list})


@app.route('/reviews', methods=['GET'])
def read_reviews():
    # 1. DB에서 리뷰 정보 모두 가져오기
    reviews = list(db.reviews.find({}, {'_id': 0}))
    # 2. 성공 여부 & 리뷰 목록 반환하기
    return jsonify({'result': 'success', 'reviews': reviews})


@app.route('/reviews', methods=['POST'])
def write_review():
    line_receive = request.form['line_give']
    # title_receive로 클라이언트가 준 title 가져오기!!!(여기 다시 확인)
    station_receive = request.form['station_give']
    # review_receive로 클라이언트가 준 review 가져오기
    review_receive = request.form['review_give']

    # DB에 삽입할 review 만들기
    review = {
        'line': line_receive,
        'station': station_receive,
        'review': review_receive
    }
    # reviews에 review 저장하기
    db.reviews.insert_one(review)
    # 성공 여부 & 성공 메시지 반환
    return jsonify({'result': 'success', 'msg': '리뷰가 성공적으로 작성되었습니다.'})


if __name__ == '__main__':
    app.run('localhost', port=5000, debug=True)
