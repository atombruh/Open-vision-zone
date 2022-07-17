import flask
from flask import *

from flask_sqlalchemy import *
from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import *
from wtforms.validators import *
from flask_login import *
from werkzeug.security import generate_password_hash , check_password_hash








app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.db'
#app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:nirupan123@localhost/students'
app.config['SECRET_KEY'] = 'keyverysecret'




db = SQLAlchemy(app)

class Students(db.Model,UserMixin):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(100),nullable=False)
    email = db.Column(db.String(200),nullable=False,unique=True)
    password_hash = db.Column(db.String(200))

    def __repr__(self):
        return '<Name %r>' % self.name





login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return Students.query.get(int(user_id))


class SignUpForm(FlaskForm):
    name = StringField('Name',validators=[DataRequired()],render_kw={"placeholder":"Name"})
    email = EmailField('Email Adress',validators=[DataRequired()],render_kw={"placeholder":"Email"})
    password_hash =PasswordField('Password',validators=[DataRequired()],render_kw={"placeholder":"Password"})
    submit = SubmitField('Register')


class LoginForm(FlaskForm):
    email = EmailField('Email Adress',validators=[DataRequired()],render_kw={"placeholder":"Email"})
    password_hash =PasswordField('Password',validators=[DataRequired()],render_kw={"placeholder":"Password"})
    submit = SubmitField('Login')



@app.route('/')
@app.route('/home')
def home():
    return render_template("index.html")
    

@app.route('/users')
def users():
    all_users = Students.query
    
    return render_template('user.html',all_users=all_users)
    
    

@app.route('/delete/<int:id>')
def delete(id):
    user = Students.query.get_or_404(id)
    db.session.delete(user)
    db.session.commit()
    return '<h1>NIce<h1>'
    


@app.route('/about')
def about():
    return render_template('about.html')



@app.route('/dashboard')
@login_required
def dashboard():
    if current_user.is_authenticated:
        if current_user.id == 1:
            return render_template('attendance.html')
        else:
            return render_template('dashboard.html')
    else:
        flash('You are not logged in Log in to Continue')
    




@app.route('/login',methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user=Students.query.filter_by(email=form.email.data).first()
        if user:
            if check_password_hash(user.password_hash,form.password_hash.data):
                login_user(user)
                flash('Successfully logged in.')
                return redirect(url_for('dashboard'))
            else:
                flash('Wrong Parameters Try again with the correct parameters')
    return render_template('login.html',form=form)

@app.route('/logout',methods=['GET','POST'])
@login_required
def logout():
    logout_user()
    flash('User logged out')
    return redirect(url_for('home'))


@app.route('/signup', methods=['GET','POST'])
def signup():
    form = SignUpForm()
    if form.validate_on_submit():
        user = Students.query.filter_by(email=form.email.data).first()
        if user is None:
            hashed_pass = generate_password_hash(form.password_hash.data)
            user = Students(name=form.name.data , email=form.email.data,password_hash=hashed_pass)
            db.session.add(user)
            db.session.commit()
            login_user(user)
            flash('Successfully signed up')
            return redirect(url_for('home'))
            
        else:
            flash('User Already registered')
    return render_template('signup.html',form=form)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html') , 404



if __name__ == '__main__':
    app.run(debug=True)