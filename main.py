from flask import Flask, render_template, request, redirect, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, LoginManager
import bcrypt

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db"
app.config["SECRET_KEY"] = "adKawjjj88919"
db = SQLAlchemy(app)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True)
    username = db.Column(db.String(255), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    
    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
    def checkpw(self, password):
        return bcrypt.checkpw(password.encode('utf-8'), self.password.encode('utf-8'))

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
        return redirect('/login')
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
        return render_template('record.html',user=user)
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