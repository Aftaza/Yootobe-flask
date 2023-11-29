from flask import Flask, render_template, request, redirect, session
from model.models import db, User, VideoYT
from lib.api import Api
from datetime import datetime
import re

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config["SECRET_KEY"] = "adKawjjj88919"
db.init_app(app)

with app.app_context():
    db.create_all()

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/admin-login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        user = User.query.filter_by(username=username).first()
        
        if user and user.checkpw(password):
            session['username'] = user.username
            return redirect('/dashboard')
        else:
            return render_template('admin_login.html',error='Invalid user')
    elif session.get('username'):
        return redirect('/dashboard')
    else:
        return render_template('admin_login.html')

@app.route('/admin-register',methods=['GET','POST'])
def admin_register():
    if request.method == 'POST':
        # handle request
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        new_user = User(username=username,email=email,password=password)
        db.session.add(new_user)
        db.session.commit()
        return redirect('/admin-login')
    return render_template('admin_register.html')

@app.route('/dashboard')
def dashboard():
    if session.get('username'):
        user = User.query.filter_by(username=session['username']).first()
        return render_template('dashboard.html',user=user)
    else:
        return redirect('/admin-login')

@app.route('/video-record')
def video_record():
    if session.get('username'):
        user = User.query.filter_by(username=session['username']).first()
        videos = VideoYT.query.all()
        return render_template('record.html',user=user, videos=videos)
    else:
        return redirect('/admin-login')

@app.route('/new-record', methods=['POST'])
def new_record():
    if session.get('username'):
        url = request.form['url']
        id = re.findall(r"v=([a-zA-Z0-9_-]{8,11})", url)
        data = Api(id[0])
        new_record = VideoYT(title=data[0], channel=data[1], views=data[2], date=datetime.fromisoformat(data[3]), link=url, thumbnail=data[4])
        db.session.add(new_record)
        db.session.commit()
        return redirect('/video-record')
    else:
        return redirect('/admin-login')

@app.route('/admin-users')
def admin_users():
    if session.get('username'):
        user = User.query.filter_by(username=session['username']).first()
        return render_template('users.html',user=user)
    else:
        return redirect('/admin-login')

@app.route('/logout')
def logout():
    session.pop('username',None)
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)