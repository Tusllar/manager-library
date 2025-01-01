from datetime import timezone
from enum import unique
from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func
from datetime import datetime

# class Note(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     data = db.Column(db.String(10000))
#     date = db.Column(db.DateTime(timezone=True), default=func.now())
#     user_id = db.Column(db.Integer, db.ForeignKey("user.id"))


class User_infor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(150))
    email = db.Column(db.String(150), unique=True)
    age = db.Column(db.Integer)  
    c_class = db.Column(db.String(150))
    phone = db.Column(db.String(150))
    gender = db.Column(db.String(150))
    address = db.Column(db.String(200))  # Thêm cột address
    avatar_url = db.Column(db.String(200), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    user = db.relationship("User", back_populates="user_infor", uselist=False)

class Class(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), unique=True)  # Tên lớp
    description = db.Column(db.String(500))  # Mô tả về lớp
    users = db.relationship('User', secondary='user_class', back_populates='classes')

class UserClass(db.Model):
    __tablename__ = 'user_class'
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    class_id = db.Column(db.Integer, db.ForeignKey('class.id'), primary_key=True)    

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(250))
    user_name = db.Column(db.String(150))
    role = db.Column(db.String(50))
    classes = db.relationship('Class', secondary='user_class', back_populates='users')
    user_infor = db.relationship("User_infor", back_populates="user", uselist=False)
    files = db.relationship("File", back_populates="user")
    def __init__(self, email, password, user_name,role):
        self.email = email
        self.password = password
        self.user_name = user_name
        self.role = role

class File(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # idfile = db.Column(db.String(150), unique=True)  # Unique ID for the file
    gvhd = db.Column(db.String(150))
    title = db.Column(db.String(150))
    title1 = db.Column(db.String(150))
    title2 = db.Column(db.String(150))
    loai = db.Column(db.String(150))
    lop = db.Column(db.String(150))
    khoa = db.Column(db.String(200))
    filename = db.Column(db.String(150))
    filetype = db.Column(db.String(100))
    link = db.Column(db.String(200))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    file_id = db.Column(db.String(200))
    link_convert = db.Column(db.String(200))
    # file_id_convert = db.Column(db.String(200))
    file_word = db.Column(db.String(200))
    status = db.Column(db.String(50), default='pending') 
    upload_time = db.Column(db.DateTime, default=datetime.utcnow)
    approval_time = db.Column(db.DateTime, nullable=True) 
    user = db.relationship("User", back_populates="files")
    # link = db.Column(db.String(150))

class Server(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    gvhd = db.Column(db.String(150))
    filename = db.Column(db.String(150))
    title = db.Column(db.String(150))
    title1 = db.Column(db.String(150))
    title2 = db.Column(db.String(150))
    status = db.Column(db.String(50), default='pending') 
    loai = db.Column(db.String(150))
    lop = db.Column(db.String(150))
    khoa = db.Column(db.String(200))
    link = db.Column(db.String(150))
