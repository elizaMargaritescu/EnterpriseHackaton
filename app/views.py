from flask import render_template, flash, redirect, session, request, url_for, make_response, Markup
from flask_admin.contrib.sqla import ModelView
import sqlite3 as lite
from sqlite3 import Error
from app import app, db, admin, models
from .models import Customer, Purchase, Posts
from datetime import timedelta
from datetime import datetime
from .forms import createCustomerform, login
import json
import os
from werkzeug.utils import secure_filename
import hashlib
import numpy as np

#adding the models to flask admin
admin.add_view(ModelView(Customer, db.session))
#the purchase table has been added, because one of the features I wanted to implement was booking tickets for online events,
#in order to be able to create graphs for our company to see with what content the users are engaging the most
admin.add_view(ModelView(Purchase, db.session))
admin.add_view(ModelView(Posts, db.session))


# landing page
@app.route('/')
def homepage():
        return render_template('index.html', title='Simple template example')

# LIST OF VALID LOG INS:
# Customer1 customer1@gmail.com customer1 
# Customer2 customer2@gmail.com customer2

# log in page
@app.route('/Login', methods=['GET', 'POST'])
def userLogin():
        error = None                
        if request.method == 'POST':
                if not request.form.get('email'):
                        error = 'EMAIL NOT ENTERED'
                else:
                        p = request.form.get('email')
                        con = lite.connect('app.db')
                        #decode the hashed password for comparison against the one entered by the user
                        compare = hashlib.sha1(request.form['password'].encode()).hexdigest()
                        with con:
                                data = con.cursor()
                                data.execute("SELECT password, id FROM Customer WHERE email=?", (p,))
                                user = data.fetchall()
                        if len(user) != 0:
                                if      compare != user[0][0]:
                                        error = 'INVALID LOGIN'
                                else:
                                        session['variable'] = user[0][1]
                                        error = 'VALID LOGIN'
                                        return redirect("/Homepage")
                        else:
                                error = 'INVALID LOGIN'

        return render_template('login.html', title = 'Login', error=error)

# Processes all the data for registering and changes the database
@app.route('/CreateAccount', methods=['GET', 'POST'])
def createCustomer():
        error = None
        if request.method == "POST":
                # Checks all values are here and correct
                con = lite.connect('app.db')

                if not request.form.get("password"):
                    error = 'You must enter a password!'

                elif not request.form.get("email"):
                    error = 'You must enter an email!'
            
                elif not request.form.get("age"):
                    error = 'You must enter an age!'

                else:
                        # name is optional, users can chose to remain anonymous
                        if request.form.get("name"):
                                name = request.form.get("name")
                        else:
                                name = "Anonym"
                        password = request.form.get("password")
                        email = request.form.get("email")
                        age = request.form.get("age")
                        #encrypting passwords for security
                        password = hashlib.sha1(password.encode()).hexdigest()
                        # Inserts data into database
                        with con:
                                data = con.cursor()
                                data.execute("SELECT email FROM Customer WHERE email=?", (email,))
                                user = data.fetchall()
                                if (len(user) > 0):
                                        error = 'EMAIL ALREADY EXISTS WITH AN ACCOUNT.'
                                else:
                                        data.execute("INSERT INTO Customer (name, email, password, age) VALUES ('{}', '{}', '{}', '{}');"
                                                        .format(name, email, password, age))
                                        return redirect('/Login')

    
        return render_template('createCustomer.html', title = 'CreateCustomer', error=error)

@app.route('/Homepage', methods=['GET', 'POST'])
def landingpage():
    parsedInfo = []
    parsedInfoPosts = []
    
    if 'variable' in session:
     
                session_id = session['variable']
                curUser = models.Customer.query.filter_by(id=session_id).first()
                posts = Posts.query.all()
                
                path = str(curUser.id) + ".png"
                

                parsedInfo.append({
                                "user_id" : curUser.id,
                                "name" : curUser.name,
                                "age": curUser.age,
                                "imageCode": path,
                                
                        })

                for i in posts:
                        print(i)
                        path2 = "post" + str(i.postId) + ".jpg"
                        print(path2)
                        parsedInfoPosts.append({
                                "postingTime" : i.postingTime,
                                "description" : i.description,
                                "likes": i.likes,
                                "tags": i.tags,
                                "path" : path2,
                        })
           
                #for the tags
                con = lite.connect('app.db')
                rows = []
                #getting the records from the database
                with con:
                                    data = con.cursor()
                                    query = data.execute("SELECT tags FROM Posts;")
                                    postings = data.fetchall()
                        
                for p in postings:
                    rows.append(p)
                joinedList = []
                #splitting the strings
                for i in range(len(rows)):
                    #concatenate the lists
                    joinedList = rows[i-1][0].split() + joinedList
                #removing duplicates from the list
                joinedList = list(dict.fromkeys(joinedList))
                print(joinedList)
    else:
                return 'Login to view purchased tickets'
    return render_template("homepage.html", user=parsedInfo, posts=parsedInfoPosts, tags = joinedList)
  
  
@app.route('/SelectTag', methods=['POST'])
def getSelectedTag():
        data = json.loads(request.data)
        session["selectedTag"] = str(data.get('tag'))
        return json.dumps({'status': 'OK'})

@app.route('/Feed', methods=['GET', 'POST'])
def myfeed():
    parsedInfo = []
    parsedInfoPosts = []
    if request.method == 'GET':
        if 'variable' in session:
                
                tag = session['selectedTag']
                
                session_id = session['variable']
                curUser = models.Customer.query.filter_by(id=session_id).first()
                posts = Posts.query.all()
                
                path = str(curUser.id) + ".png"

                parsedInfo.append({
                                "user_id" : curUser.id,
                                "name" : curUser.name,
                                "age": curUser.age,
                                "imageCode": path,
                                
                        })

                for i in posts:
                        print(((i.tags).split())[0])
                        print(((i.tags).split())[1])
                        for m in range(len((i.tags).split())):

                            if(((i.tags).split())[m-1] == tag):
                                
                                path2 = "post" + str(i.postId) + ".jpg"
                                parsedInfoPosts.append({
                                        "postingTime" : i.postingTime,
                                        "description" : i.description,
                                        "likes": i.likes,
                                        "tags": i.tags,
                                        "path" : path2,
                                })
                #for the tags
                con = lite.connect('app.db')
                rows = []
                #getting the records from the database
                with con:
                                    data = con.cursor()
                                    query = data.execute("SELECT tags FROM Posts;")
                                    postings = data.fetchall()
                        
                for p in postings:
                    rows.append(p)
                joinedList = []
                #splitting the strings
                for i in range(len(rows)):
                    #concatenate the lists
                    joinedList = rows[i-1][0].split() + joinedList
                #removing duplicates from the list
                joinedList = list(dict.fromkeys(joinedList))
                print(joinedList)
                return render_template("myfeed.html", posts=parsedInfoPosts, user=parsedInfo, tags = joinedList)
        else:
                return 'log in first'

@app.route('/Calendar', methods=['GET', 'POST'])
def whatsOn():
    return render_template('calendar.html', title='what is on page')

@app.route('/AboutUs', methods=['GET', 'POST'])
def aboutUs():
    return render_template('about.html', title='mission')