#flask 라이브러리 안에 Flask 라는 객체 존재
from flask import Flask, render_template, request
from data import Articles #모듈 형식으로 data.py의 data 가져오기

app = Flask(__name__) #__name__이라는 내장변수를 받아 새로운 instance인 app 생성
app.debug = True #파일 저장할 때마다 서버 restart하려면 debug 설정 추가

@app.route('/', methods=['GET', 'POST']) # @: decorate
def hello_world(): #함수 생성
    # return 'Hello World!'
    # return render_template('index.html', data = "안녕하세요 김태경 입니다.")
    
    articles = Articles() #articles는 리스트
    # print(articles)
    
    # return render_template('index.html', data = "Main Page")

    for i in articles:
        print(i['title'])
    return render_template('index.html', articles = articles)

#render_template : detail.html을 rendering
@app.route('/<id>/article', methods=['GET', 'POST'])
def detail(id):
    if request.method == 'GET':
        articles = Articles()
        print(articles[int(id)-1])
        return render_template('detail.html', article = articles[int(id)-1])



#내장변수가 name이면 다음 함수를 실행시켜라
if __name__ == '__main__':
    app.run(port=5000)

