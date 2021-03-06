from datetime import datetime, timezone, timedelta
from flaskBlog import db, login_man
from flask_login import UserMixin
import jwt
from decouple import config


@login_man.user_loader
def load_user(user_id):
    return user.query.get(int(user_id))


#try to always use lowercase class(aka models) names when using SQLAlchemy
class user(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default="default.png")
    password = db.Column(db.String(60), nullable=False)
    # 'post' references model name, hence the capitalization
    posts = db.relationship('post', backref='author', lazy=True)
    
    def get_reset_token(self, expires_sec=900):
        token = jwt.encode(
            {
                'user_id': self.id,
                'exp': (datetime.now(tz=timezone.utc) +
                        timedelta(seconds=expires_sec))
            },
            config('SECRET_KEY'),
            algorithm="HS256"
        )
        return token
    
    @staticmethod
    def verify_reset_token(token):
        try:
            user_id = jwt.decode(token, config('SECRET_KEY'), algorithms=["HS256"])['user_id']
        except jwt.exceptions.ExpiredSignatureError:
            return None
        return user.query.get(user_id)
    
    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"


class post(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(280), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.today())
    content = db.Column(db.Text, nullable=False)
    #'user.id' references table name which is automatically lowercase in SQLAlchemy
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"
