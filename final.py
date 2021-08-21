from flask import Flask,render_template,request,redirect,session,Response
from flask_mail import Mail,Message
from flask_sqlalchemy import SQLAlchemy
import pymongo
from datetime import datetime
from selenium import webdriver 
import requests
import os
from bs4 import BeautifulSoup as bs
import mysql.connector
import schedule
import time
from flask_apscheduler import APScheduler

app=Flask(__name__)
scheduler=APScheduler()
app.secret_key=os.urandom(24)

conn=mysql.connector.connect(host="localhost",user="root",password="",database="GetYourLinks.data")
cursor=conn.cursor()

mail=Mail(app)

#cursor.execute("CREATE TABLE finalcontent(user_id INTEGER PRIMARY KEY AUTO_INCREMENT,content VARCHAR(500)NOT NULL,links VARCHAR(500)NOT NULL)")
try:
    mongo=pymongo.MongoClient(
        host="localhost",
        port=27017,
        serverSelectionTimeoutMS=1000
        )
    db=mongo.allcontent
    mongo.server_info()
except:
    print("not connected")

#def deleteolddatabase():
    #for i in range(500):
        #collection=db.get_collection("users")
        #collection.delete_one({})
def deleteolddatabase():
    collection=db.get_collection("users")
    collection.delete_many({})
    
collection=db.get_collection("users")
collection.create_index([('content', 'text')])

#app.config.update(
    #MAIL_SERVER='smtp.gmai.com',
    #MAIL_PORT='465',
    #MAIL_USE_SSL=True,
    #MAIL_USERNAME='antaragetyourlinks@gmail.com',
    #MAIL_PASSWORD='getyourlinks'
#)
#mail=Mail(app)
#mail.send_message('testing', sender='antaragetyourlinks@gmail.com', recipients='missantaraghosh709@gmail.com')
def contentstoring():
    data=[]
    data1=[]
    
    s=requests.get("https://timesofindia.indiatimes.com/news")
    soup = bs(s.content,'html.parser')
    c=0
    for li in (soup.findAll("div", {"class": "main-content"})):
        for i in (soup.findAll("span", {"class": "w_tle"})):
            c=c+1
            if c>=21:
                data.append(("https://timesofindia.indiatimes.com/news")+(i.a['href']))
                data1.append(i.a.text) 
    s=requests.get("https://www.livemint.com/latest-news")
    soup = bs(s.content,'html.parser')
    for li in (soup.findAll("div", {"class": "listView"})):
        for i in (soup.findAll("h2", {"class": "headline"})):
            data.append(("https://www.livemint.com")+(i.a['href']))
            data1.append(i.text)
    s=requests.get("https://www.indiatoday.in/trending-news")
    soup = bs(s.content,'html.parser')
    for li in (soup.findAll("div", {"class": "view-content"})):
        for i in (soup.findAll("div", {"class": "catagory-listing"})):
            data.append(("https://www.indiatoday.in")+(i.a['href']))
            data1.append(i.p.text)   
    s=requests.get("https://timesofindia.indiatimes.com/news")
    soup = bs(s.content,'html.parser')
    for li in (soup.findAll("div", {"class": "main-content"})):
        for i in (soup.findAll("span", {"class": "w_tle"})):
            data.append(("https://timesofindia.indiatimes.com/news")+(i.a['href']))
            data1.append(i.a.text)   
    s=requests.get("https://www.livemint.com/mostpopular")
    soup = bs(s.content,'html.parser')
    for li in (soup.findAll("div", {"class": "listView"})):
        for i in (soup.findAll("h2", {"class": "headline"})):
            data.append(("https://www.livemint.com")+(i.a['href']))
            data1.append(i.text)
    s=requests.get("https://www.ndtv.com/education/latest-news")
    soup = bs(s.content,'html.parser')
    for li in (soup.findAll("div", {"class": "articles"})):
        for i in (soup.findAll("div", {"class": "detail"})):
            data.append(("https://www.ndtv.com")+(i.a['href']))
            data1.append(i.a.text) 
    s=requests.get("https://www.indiatoday.in/education-today/news")
    soup = bs(s.content,'html.parser')
    for li in (soup.findAll("div", {"class": "view-content"})):
        for i in (soup.findAll("div", {"class": "catagory-listing"})):
            data.append(("https://www.indiatoday.in")+(i.a['href']))
            data1.append(i.p.text)
    s=requests.get("https://timesofindia.indiatimes.com/home/education/news")
    soup = bs(s.content,'html.parser')
    c=0
    for li in (soup.findAll("ul", {"class": "list5 clearfix"})):
        for i in (soup.findAll("span", {"class": "w_tle"})):
            if c<=35:
                data.append(("https://timesofindia.indiatimes.com/news")+(i.a['href']))
                data1.append(i.a.text)
                c=c+1
            else:
                break
    s=requests.get("https://www.indiatoday.in/india")
    soup = bs(s.content,'html.parser')
    for li in (soup.findAll("div", {"class": "view-content"})):
        for i in (soup.findAll("div", {"class": "catagory-listing"})):
            data.append(("https://www.indiatoday.in")+(i.a['href']))
            data1.append(i.a.text)  
    s=requests.get("https://www.ndtv.com/india")
    soup = bs(s.content,'html.parser')
    for li in (soup.findAll("div", {"class": "lisingNews"})):
        for i in (soup.findAll("h2", {"class": "newsHdng"})):
            data.append(i.a['href'])
            data1.append(i.a.text)
    s=requests.get("https://timesofindia.indiatimes.com/india")
    soup = bs(s.content,'html.parser')
    c=0
    for li in (soup.findAll("ul", {"class": "top-newslist clearfix"})):
        for i in (soup.findAll("span", {"class": "w_tle"})):
            if c<=35:
                data.append(("https://timesofindia.indiatimes.com/news")+(i.a['href']))
                data1.append(i.a.text)
                c=c+1
            else:
                break
    s=requests.get("https://www.indiatoday.in/cities")
    soup = bs(s.content,'html.parser')
    for li in (soup.findAll("div", {"class": "view-content"})):
        for i in (soup.findAll("div", {"class": "catagory-listing"})):
            data.append(("https://www.indiatoday.in")+(i.a['href']))
            data1.append(i.p.text)   
    s=requests.get("https://www.ndtv.com/cities")
    soup = bs(s.content,'html.parser')
    for li in (soup.findAll("div", {"class": "lisingNews"})):
        for i in (soup.findAll("h2", {"class": "newsHdng"})):
            data.append(i.a['href'])
            data1.append(i.a.text)   
    s=requests.get("https://timesofindia.indiatimes.com/city")
    soup = bs(s.content,'html.parser')
    c=0
    for li in (soup.findAll("div", {"class": "top-newslist"})):
        for i in (soup.findAll("span", {"class": "w_tle"})):
            if c<=35:
                data.append(("https://timesofindia.indiatimes.com/news")+(i.a['href']))
                data1.append(i.a.text)
                c=c+1
            else:
                break 
    s=requests.get("https://www.ndtv.com/world-news")
    soup = bs(s.content,'html.parser')
    for li in (soup.findAll("div", {"class": "lisingNews"})):
        for i in (soup.findAll("h2", {"class": "newsHdng"})):
            data.append(i.a['href'])
            data1.append(i.a.text) 
    s=requests.get("https://www.indiatoday.in/world")
    soup = bs(s.content,'html.parser')
    for li in (soup.findAll("div", {"class": "catros_content"})):
        for i in (soup.findAll("div", {"class": "detail"})):
            data.append(("https://www.indiatoday.in")+(i.a['href']))
            data1.append(i.a.text)  
    s=requests.get("https://timesofindia.indiatimes.com/world")
    soup = bs(s.content,'html.parser')
    c=0
    for li in (soup.findAll("div", {"class": "top-newslist"}, {"id": "c_wdt_list_1"})):
        for i in (soup.findAll("span", {"class": "w_tle"})):
            if c<=35:
                data.append(("https://timesofindia.indiatimes.com/news")+(i.a['href']))
                data1.append(i.a.text)
                c=c+1
            else:
                break
    
    s=requests.get("https://www.ndtv.com/trends/most-popular-movies-news")
    soup = bs(s.content,'html.parser')
    for li in (soup.findAll("div", {"class": "clr"})):
        for i in (soup.findAll("p", {"class": "trenz_news_head lh22 listing_story_title"})):
            data.append(i.a['href'])
            data1.append(i.text)   
    s=requests.get("https://timesofindia.indiatimes.com/news")
    soup = bs(s.content,'html.parser')
    c=0
    for li in (soup.findAll("ul", {"class": "cvs_wdt clearfix"})):
        for i in (soup.findAll("span", {"class": "w_tle"})):
            if c<=4:
                data.append(("https://timesofindia.indiatimes.com/news")+(i.a['href']))
                data1.append(i.a.text)
                c=c+1
            else:
                break
    s=requests.get("https://www.indiatoday.in/sports/ipl2020/news")
    soup = bs(s.content,'html.parser')
    for li in (soup.findAll("div", {"class": "view-content"})):
        for i in (soup.findAll("div", {"class": "catagory-listing"})):
            data.append(("https://www.indiatoday.in")+(i.a['href']))
            data1.append(i.p.text)
    s=requests.get("https://www.ndtv.com/trends/most-popular-sports-news")
    soup = bs(s.content,'html.parser')
    for li in (soup.findAll("div", {"class": "clr"})):
        for i in (soup.findAll("p", {"class": "trenz_news_head lh22 listing_story_title"})):
            data.append(i.a['href'])
            data1.append(i.text)   
    s=requests.get("https://timesofindia.indiatimes.com/news")
    soup = bs(s.content,'html.parser')
    c=0
    for li in (soup.findAll("ul", {"class": "cvs_wdt clearfix"})):
        for i in (soup.findAll("span", {"class": "w_tle"})):
            c=c+1
            if c>15 and c<21:
                data.append(("https://timesofindia.indiatimes.com/news")+(i.a['href']))
                data1.append(i.a.text)
    
    for i in range(len(data1)):
        user={"content":data1[i],"link":data[i]}
        dbResponse=db.users.insert_one(user)
        
scheduler.add_job(id="scheduled task",func=deleteolddatabase, trigger='interval', minutes=1)
scheduler.add_job(id="scheduled task1",func=contentstoring, trigger='interval', minutes=1)
scheduler.start()
    

@app.route("/")
def home():
    return render_template('index1n.html')
 


@app.route("/newsearch")
def search():
    if 'user_id' in session:
        return render_template('newsearch.html')
    else:
        return redirect('/loginn')

@app.route("/latest")
def latest():
    data=[]
    data1=[]
    
    s=requests.get("https://timesofindia.indiatimes.com/news")
    soup = bs(s.content,'html.parser')
    c=0
    for li in (soup.findAll("div", {"class": "main-content"})):
        for i in (soup.findAll("span", {"class": "w_tle"})):
            c=c+1
            if c>=21:
                data.append(("https://timesofindia.indiatimes.com/news")+(i.a['href']))
                data1.append(i.a.text)    
    s=requests.get("https://www.livemint.com/latest-news")
    soup = bs(s.content,'html.parser')
    for li in (soup.findAll("div", {"class": "listView"})):
        for i in (soup.findAll("h2", {"class": "headline"})):
            data.append(("https://www.livemint.com")+(i.a['href']))
            data1.append(i.text)
    #for i in range(len(data1)):
        #cursor.execute("INSERT INTO finalcontent(user_id,content,links) VALUES(NULL,%s,%s)",(data1[i],data[i]))
        #cursor.execute("""INSERT INTO `content3`(`user_id`,`content`,`links`)VALUES(NULL,'{}','{}')""".format(data1[i],data[i]))
    #conn.commit()
    
    length=len(data)
    return render_template('latest.html',r1=data,r2=data1,l=length)

@app.route("/trending")
def trending():
    data=[]
    data1=[]
    s=requests.get("https://www.indiatoday.in/trending-news")
    soup = bs(s.content,'html.parser')
    for li in (soup.findAll("div", {"class": "view-content"})):
        for i in (soup.findAll("div", {"class": "catagory-listing"})):
            data.append(("https://www.indiatoday.in")+(i.a['href']))
            data1.append(i.p.text)   
    s=requests.get("https://timesofindia.indiatimes.com/news")
    soup = bs(s.content,'html.parser')
    for li in (soup.findAll("div", {"class": "main-content"})):
        for i in (soup.findAll("span", {"class": "w_tle"})):
            data.append(("https://timesofindia.indiatimes.com/news")+(i.a['href']))
            data1.append(i.a.text)   
    s=requests.get("https://www.livemint.com/mostpopular")
    soup = bs(s.content,'html.parser')
    for li in (soup.findAll("div", {"class": "listView"})):
        for i in (soup.findAll("h2", {"class": "headline"})):
            data.append(("https://www.livemint.com")+(i.a['href']))
            data1.append(i.text)   
    
    length=len(data)
    return render_template('trending.html',r1=data,r2=data1,l=length)
    
@app.route("/education")
def education():
    data=[]
    data1=[]
    s=requests.get("https://www.ndtv.com/education/latest-news")
    soup = bs(s.content,'html.parser')
    for li in (soup.findAll("div", {"class": "articles"})):
        for i in (soup.findAll("div", {"class": "detail"})):
            data.append(("https://www.ndtv.com")+(i.a['href']))
            data1.append(i.a.text) 
    s=requests.get("https://www.indiatoday.in/education-today/news")
    soup = bs(s.content,'html.parser')
    for li in (soup.findAll("div", {"class": "view-content"})):
        for i in (soup.findAll("div", {"class": "catagory-listing"})):
            data.append(("https://www.indiatoday.in")+(i.a['href']))
            data1.append(i.p.text)
    s=requests.get("https://timesofindia.indiatimes.com/home/education/news")
    soup = bs(s.content,'html.parser')
    c=0
    for li in (soup.findAll("ul", {"class": "list5 clearfix"})):
        for i in (soup.findAll("span", {"class": "w_tle"})):
            if c<=35:
                data.append(("https://timesofindia.indiatimes.com/news")+(i.a['href']))
                data1.append(i.a.text)
                c=c+1
            else:
                break
      
    
    length=len(data)
    return render_template('education.html',r1=data,r2=data1,l=length)

@app.route("/india")
def india():
    data=[]
    data1=[]
    s=requests.get("https://www.indiatoday.in/india")
    soup = bs(s.content,'html.parser')
    for li in (soup.findAll("div", {"class": "view-content"})):
        for i in (soup.findAll("div", {"class": "catagory-listing"})):
            data.append(("https://www.indiatoday.in")+(i.a['href']))
            data1.append(i.a.text)  
    s=requests.get("https://www.ndtv.com/india")
    soup = bs(s.content,'html.parser')
    for li in (soup.findAll("div", {"class": "lisingNews"})):
        for i in (soup.findAll("h2", {"class": "newsHdng"})):
            data.append(i.a['href'])
            data1.append(i.a.text)
    s=requests.get("https://timesofindia.indiatimes.com/india")
    soup = bs(s.content,'html.parser')
    c=0
    for li in (soup.findAll("ul", {"class": "top-newslist clearfix"})):
        for i in (soup.findAll("span", {"class": "w_tle"})):
            if c<=35:
                data.append(("https://timesofindia.indiatimes.com/news")+(i.a['href']))
                data1.append(i.a.text)
                c=c+1
            else:
                break
    
    length=len(data)
    return render_template('india.html',r1=data,r2=data1,l=length)

@app.route("/cities")
def cities():
    data=[]
    data1=[]
    s=requests.get("https://www.indiatoday.in/cities")
    soup = bs(s.content,'html.parser')
    for li in (soup.findAll("div", {"class": "view-content"})):
        for i in (soup.findAll("div", {"class": "catagory-listing"})):
            data.append(("https://www.indiatoday.in")+(i.a['href']))
            data1.append(i.p.text)   
    s=requests.get("https://www.ndtv.com/cities")
    soup = bs(s.content,'html.parser')
    for li in (soup.findAll("div", {"class": "lisingNews"})):
        for i in (soup.findAll("h2", {"class": "newsHdng"})):
            data.append(i.a['href'])
            data1.append(i.a.text)   
    s=requests.get("https://timesofindia.indiatimes.com/city")
    soup = bs(s.content,'html.parser')
    c=0
    for li in (soup.findAll("div", {"class": "top-newslist"})):
        for i in (soup.findAll("span", {"class": "w_tle"})):
            if c<=35:
                data.append(("https://timesofindia.indiatimes.com/news")+(i.a['href']))
                data1.append(i.a.text)
                c=c+1
            else:
                break
    
    length=len(data)
    return render_template('cities.html',r1=data,r2=data1,l=length)
    
@app.route("/world")
def world():
    data=[]
    data1=[]
    s=requests.get("https://www.ndtv.com/world-news")
    soup = bs(s.content,'html.parser')
    for li in (soup.findAll("div", {"class": "lisingNews"})):
        for i in (soup.findAll("h2", {"class": "newsHdng"})):
            data.append(i.a['href'])
            data1.append(i.a.text) 
    s=requests.get("https://www.indiatoday.in/world")
    soup = bs(s.content,'html.parser')
    for li in (soup.findAll("div", {"class": "catros_content"})):
        for i in (soup.findAll("div", {"class": "detail"})):
            data.append(("https://www.indiatoday.in")+(i.a['href']))
            data1.append(i.a.text)  
    s=requests.get("https://timesofindia.indiatimes.com/world")
    soup = bs(s.content,'html.parser')
    c=0
    for li in (soup.findAll("div", {"class": "top-newslist"}, {"id": "c_wdt_list_1"})):
        for i in (soup.findAll("span", {"class": "w_tle"})):
            if c<=35:
                data.append(("https://timesofindia.indiatimes.com/news")+(i.a['href']))
                data1.append(i.a.text)
                c=c+1
            else:
                break
    
    length=len(data)
    return render_template('world.html',r1=data,r2=data1,l=length)
    
@app.route("/entertainment")
def entertainment():
    data=[]
    data1=[]
    s=requests.get("https://www.ndtv.com/trends/most-popular-movies-news")
    soup = bs(s.content,'html.parser')
    for li in (soup.findAll("div", {"class": "clr"})):
        for i in (soup.findAll("p", {"class": "trenz_news_head lh22 listing_story_title"})):
            data.append(i.a['href'])
            data1.append(i.text)   
    s=requests.get("https://timesofindia.indiatimes.com/news")
    soup = bs(s.content,'html.parser')
    c=0
    for li in (soup.findAll("ul", {"class": "cvs_wdt clearfix"})):
        for i in (soup.findAll("span", {"class": "w_tle"})):
            if c<=4:
                data.append(("https://timesofindia.indiatimes.com/news")+(i.a['href']))
                data1.append(i.a.text)
                c=c+1
            else:
                break
    
    length=len(data)
    return render_template('entertainment.html',r1=data,r2=data1,l=length)
    
@app.route("/sports")
def sports():
    data=[]
    data1=[]
    s=requests.get("https://www.indiatoday.in/sports/ipl2020/news")
    soup = bs(s.content,'html.parser')
    for li in (soup.findAll("div", {"class": "view-content"})):
        for i in (soup.findAll("div", {"class": "catagory-listing"})):
            data.append(("https://www.indiatoday.in")+(i.a['href']))
            data1.append(i.p.text)
    s=requests.get("https://www.ndtv.com/trends/most-popular-sports-news")
    soup = bs(s.content,'html.parser')
    for li in (soup.findAll("div", {"class": "clr"})):
        for i in (soup.findAll("p", {"class": "trenz_news_head lh22 listing_story_title"})):
            data.append(i.a['href'])
            data1.append(i.text)   
    s=requests.get("https://timesofindia.indiatimes.com/news")
    soup = bs(s.content,'html.parser')
    c=0
    for li in (soup.findAll("ul", {"class": "cvs_wdt clearfix"})):
        for i in (soup.findAll("span", {"class": "w_tle"})):
            c=c+1
            if c>15 and c<21:
                data.append(("https://timesofindia.indiatimes.com/news")+(i.a['href']))
                data1.append(i.a.text)
    
    length=len(data)
    return render_template('sports.html',r1=data,r2=data1,l=length)
    
    
@app.route("/result", methods=['POST'])
def getvalue():        
    url=request.form['search']
    pp=collection.find({"$text":{"$search":url}})
    data=[]
    data1=[]
    for result in pp:
        data1.append(result["content"])
        data.append(result["link"])
    
    if not data:
        data.append("  ")
        data1.append(("no results found for   ")+(url))
    length=len(data)
    print(length)
    return render_template('result.html',r1=data,r2=data1,l=length)
    
@app.route("/loginn")
def login():
    return render_template('loginn.html')
@app.route("/loginvalue", methods=['POST'])
def loginvalue():
    email=request.form.get('email')
    password=request.form.get('password')
    cursor.execute("""SELECT * FROM `usersdata1` WHERE `email` LIKE '{}' AND `password` LIKE '{}'""".format(email,password))
    user=cursor.fetchall()
    if len(user)>0:
        session['user_id']=user[0][0]
        return redirect('/')
    else:
        return redirect('/loginn')
@app.route("/signupvalue", methods=['POST'])
def signupvalue():
    name=request.form.get('username')
    email=request.form.get('semail')
    password=request.form.get('spsw')

    cursor.execute("""INSERT INTO `usersdata1`(`user_id`,`name`,`email`,`password`)VALUES(NULL,'{}','{}','{}')""".format(name,email,password))
    conn.commit()
    cursor.execute("""SELECT*FROM `usersdata1` WHERE `email` LIKE '{}'""".format(email))
    mycursor=cursor.fetchall()
    session['user_id']=mycursor[0][0]
    return redirect('/loginn')
@app.route("/signupn")
def signup():
    return render_template('signupn.html')

@app.route('/logout')
def logout():
    if 'user_id' in session:
        session.pop('user_id')
        return redirect('/')
    else:
        return redirect('/loginn')
@app.route('/service')
def service():
    return render_template('service.html')
app.run(debug=False)
