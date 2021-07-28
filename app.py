#flask 라이브러리 안에 Flask 라는 객체 존재
from flask import Flask, render_template, request, redirect, session
from data import Articles #모듈 형식으로 data.py의 data 가져오기
import pymysql
from passlib.hash import pbkdf2_sha256

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

@app.route('/')
def main():
    return render_template('index.html')

@app.route('/articles', methods=['GET', 'POST']) # @: decorate
def articles(): #함수 생성
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
    return render_template('articles.html', articles = articles)

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

@app.route('/<id>/edit', methods=['GET','POST'])
def edit_article(id):
    if request.method == 'GET':
        sql= f"SELECT * FROM lists WHERE id = {int(id)};"
        # print(sql)

        # SQL query 실행
        cursor.execute(sql)
        article = cursor.fetchone()

        return render_template('edit_article.html', article = article)
    elif request.method == "POST":
        title = request.form['title']
        description = request.form['description']
        author = request.form['author']
        
        # SQL query 작성
        # sql= f"""UPDATE lists SET title='{title}', description='{description}' , author='{author}'
        #  WHERE id = {int(id)} """
        sql= """UPDATE lists SET title='%s', description='%s' , author='%s'
         WHERE id = %d """ % (title,description,author,int(id))
        # print(sql)

        # SQL query 실행
        cursor.execute(sql)
        
        # 데이터 변화 적용
        db.commit()

        return redirect('/')

#form 체크할 수 있는 라이브러리 추가
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, EqualTo

class RegisterForm(FlaskForm):
    id = StringField('ID', validators=[DataRequired()])
    name = StringField('NAME', validators=[DataRequired()])
    email = StringField('EMAIL', validators=[DataRequired()])
    phone = StringField('PHONE NUMBER', validators=[DataRequired()])
    password = PasswordField('PASSWORD', validators=[DataRequired()]) #equalTo("필드네임")
    repassword = PasswordField('REPASSWORD', validators=[DataRequired(), EqualTo('password', message="test")])
    submit = SubmitField("Signup")
# id가 들어왔는지 확인하고 비밀번호 확인

@app.route('/register', methods=['GET','POST'])
def register():
    form = RegisterForm()
    if request.method == 'GET':
        return render_template('register.html', form = form)
    elif request.method == 'POST':
        if form.validate_on_submit():
            user_id = request.form['id'] #두 가지 방법 있음 -1.form 인덱싱
            name = request.form.get('name') #2.get방식
            email = request.form['email']
            phone = request.form['phone']
            password = pbkdf2_sha256.hash(request.form['password'])
            sql = f"SELECT user_id FROM users WHERE user_id = '{user_id}'"
        
            cursor.execute(sql)
            user = cursor.fetchone()
            
            if user != None:
                return render_template('register.html', form = form)
            else:
                sql = f"""INSERT INTO users(user_id, name, email, phone, password)
                VALUES('{user_id}','{name}','{email}','{phone}','{password}');"""
                cursor.execute(sql)

                db.commit()
                return "SUCCESS"
        else:
            return render_template('register.html', form = form)

@app.route('/login', methods=['GET','POST'])
def login():
    if request.method == "GET":
        return render_template('login.html')
    else:
        user_id = request.form['id']
        password = request.form['password']

        sql = f"SELECT * FROM users WHERE user_id = '{user_id}'"

        cursor.execute(sql)

        user = cursor.fetchone()
        print(user)
        if user == None:
            return render_template('login.html')
        else:
            user_db_pw = user[5]
            result = pbkdf2_sha256.verify(password, user_db_pw)
            if result:
                session['is_loged'] = True
                session['username'] = user[2]
                return render_template('index.html', username = session['username'])
            else:
                return render_template('login.html')

#내장변수가 name이면 다음 함수를 실행시켜라
if __name__ == '__main__':
    app.config['SECRET_KEY']="secret"
    app.run(port=5000)



