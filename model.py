# THIS FILE IS ONLY MADE UP FOR THE MODEL CONTAINING
#import packages
from flask import Flask,render_template,request,session
from flask_sqlalchemy import SQLAlchemy
#this pakacge will check the userr state like activation, anoymous, and authentication bu default
from flask_login import UserMixin
#this package will genrate  and check password
from werkzeug.security import generate_password_hash,check_password_hash
#it will manage the user login
from flask_login import LoginManager
#use to identify uniqelly data
from enum import unique



db = SQLAlchemy()

#create the object of login manager to manage the login
login = LoginManager()

#create the module for USER which will be inheritaed by UserMixin and model class
class UserModel(UserMixin,db.Model):
    #giving the table name
    __tablename__ = 'users'
    
    id = db.Column(db.Integer,primary_key=True)
    email = db.Column(db.String(50),unique=True,nullable= False)
    username = db.Column(db.String(50))
    password_hash = db.Column(db.String(250))
    
    #convert the password into hashing
    def set_password(self,password):
        self.password_hash = generate_password_hash(password)
    
    #check the password during login if password match then true else false
    def check_password(self,password):
        return check_password_hash(self.password_hash,password)
    
#create the module for CATEGORY 
class CategoryMaster(db.Model):
    category_id = db.Column(db.Integer,primary_key=True)
    category_name = db.Column(db.String(100),nullable=False)
    blog = db.relationship('BlogModel',backref = 'categorymaster',lazy=True)

#craete module for BLOGs 
class BlogModel(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    category_id = db.Column(db.Integer,db.ForeignKey('category_master.category_id'),nullable=False)
    blog_user_id = db.Column(db.Integer,db.ForeignKey('users.id'),nullable = False)
    blog_cont = db.Column(db.Text,nullable = False)
    blog_date = db.Column(db.DateTime)
    blog_readcount = db.Column(db.Integer,default = 0)
    blog_ratecount = db.Column(db.Integer,default = 0)
    
class BlogComment(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    blog_id = db.Column(db.Integer,db.ForeignKey('blog_model.id'),nullable=False)
    blog_comment = db.Column(db.Text)
    commnet_userid = db.Column(db.Integer,db.ForeignKey('users.id'),nullable = False)
    blog_rate = db.Column(db.Integer)
    blog_comment_date = db.Column(db.DateTime)
    
@login.user_loader 
def load_user(id):
    return UserModel.query.get(int(id))

