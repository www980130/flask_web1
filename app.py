#flask 라이브러리 안에 Flask 라는 객체 존재
from flask import Flask, render_template, request, redirect
from data import Articles #모듈 형식으로 data.py의 data 가져오기
import pymysql

app = Flask(__name__) #__name__이라는 내장변수를 받아 새로운 instance인 app 생성
app.debug = True #파일 저장할 때마다 서버 restart하려면 debug 설정 추가

# database에 접근
db= pymysql.connect(host='localhost',
                     port=3306,
                     user='root',
                     passwd='agee04041**',
                     db='o2',
                     charset='utf8')

# database를 사용하기 위한 cursor를 세팅합니다.
cursor= db.cursor() 


@app.route('/', methods=['GET', 'POST']) # @: decorate
def hello_world(): #함수 생성
    # return 'Hello World!'
    # return render_template('index.html', data = "안녕하세요 김태경 입니다.")
    
    articles = Articles() #articles는 리스트
    # print(articles)
    
    sql= f"SELECT * FROM lists;"
    # print(sql)

    # SQL query 실행
    cursor.execute(sql)
    articles = cursor.fetchall()
    # print(articles[0][1]) #data는 tuple 형태

    # return render_template('index.html', data = "Main Page")

    # for i in articles:
        # print(i['title'])
        # print(i[1])
    return render_template('index.html', articles = articles)

#render_template : detail.html을 rendering
@app.route('/<id>/article', methods=['GET', 'POST'])
def detail(id):
    if request.method == 'GET':
        # articles = Articles()
        # print(articles[int(id)-1])
        sql= f"SELECT * FROM lists WHERE id = {int(id)};"
        # print(sql)

        # SQL query 실행
        cursor.execute(sql)
        article = cursor.fetchone() #fetchall하면 indexing 2번 됨 
        print(article)
        return render_template('detail.html', article = article)
        # return render_template('detail.html', article = articles[int(id)-1])

@app.route('/article/add', methods=['GET','POST'])
def add_article():
    if request.method == 'GET':
        return render_template('add_article.html')
    elif request.method == 'POST':
        # print(request.form) # >>ImmutableMultiDict([('test', 'kim'), ('work', 'insert')])])
        # print(request.form.get('test')) # >>kim
        title = request.form['title']
        description = request.form['description']
        author = request.form['author']
        
        # SQL query 작성
        sql= f"""INSERT INTO lists(title, description, author) 
        VALUES('{title}', '{description}', '{author}');"""
        # print(sql)

        # SQL query 실행
        cursor.execute(sql)
        
        # 데이터 변화 적용
        db.commit()


        return redirect('/')

@app.route('/<id>/delete', methods=['GET'])
def del_article(id):
    # SQL query 작성
    sql= f"DELETE FROM `o2`.`lists` WHERE(`id` = '{int(id)}')"
    # print(sql)

    # SQL query 실행
    cursor.execute(sql)
    
    # 데이터 변화 적용
    db.commit()
    return redirect('/')


#내장변수가 name이면 다음 함수를 실행시켜라
if __name__ == '__main__':
    app.run(port=5000)

