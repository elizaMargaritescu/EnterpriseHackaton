from app import db
import sqlite3 as lite

purchasing = db.Table('purchasing', db.Model.metadata,
                      db.Column('id', db.Integer, db.ForeignKey('customer.id')),
                      db.Column('ticketId', db.Integer, db.ForeignKey('purchase.ticketId')))
                    

class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), index=True)
    email = db.Column(db.String(50), index=True)
    password = db.Column(db.String(50), index=True)
    phone = db.Column(db.String(11), index=True)
    age = db.Column(db.Integer, index=True)
    #tickets for events, scheduled guest speakers
    purchases = db.relationship('Purchase', secondary = purchasing) 
    postsCustomer = db.Column(db.Integer, db.ForeignKey('posts.postId'))

class Purchase(db.Model):
    ticketId = db.Column(db.Integer, primary_key=True)
    dateAndTime = db.Column(db.DateTime, index=True)
    customers = db.relationship('Customer', secondary = purchasing)

class Posts(db.Model):
    postId = db.Column(db.Integer, primary_key=True)
    postingTime = db.Column(db.DateTime, index=True)
    description = db.Column(db.String(200), index=True)
    likes = db.Column(db.Integer, index=True)
    customersPosts = db.relationship('Customer', backref='details', lazy='dynamic')





db.create_all()