from flask import Flask, request, render_template, jsonify, g
import os, psycopg2
from psycopg2.extras import RealDictCursor
from sqlalchemy import create_engine
from bs4 import BeautifulSoup
import requests, datetime, re
import pandas as pd
import urllib.parse

app = Flask(__name__)

# DATABASE SECTION
#
# Connecting technique mostly taken from
# http://flask.pocoo.org/docs/dev/tutorial/dbcon/
def connect_db():
  # If there's something in the os.environ, connect
  # otherwise use the hard-coded version
  # (this is a terrible practice)
  if os.environ.get('DATABASE_URL'):
    database_url = os.environ.get('DATABASE_URL')
    db = psycopg2.connect(database_url)
  else:
    database_url = ""
    db = psycopg2.connect(database_url)
  return db

def get_db():
  if not hasattr(g, 'db'):
    g.db = connect_db()
  return g.db

@app.teardown_appcontext
def teardown_db(error):
  if hasattr(g, 'db'):
    g.db.close()

# ACTUAL APP

@app.route("/")
def index():
  return render_template("main.html")

@app.route('/', methods=['POST'])
def my_form_post():
  text = request.form['user_name']
  processed_text = text.upper()
  return processed_text



















# THIS IS THE ORIGINAL SUBMIT BUTTON
# EDITED: changed the route to immediate
# NOW CALLED Send Now

@app.route('/immediate', methods = ["POST", "GET"])
def immediate():
  if request.method == "POST":
    result = request.form


  # saving user info to variables
  user_info_list = list(result.items())
  
  user_email = str(user_info_list[0][1])
  
  user_topic = str(user_info_list[1][1])
  user_search_params = {'q': user_topic}
  user_url_search_terms = urllib.parse.urlencode(user_search_params)
  
  




  response = requests.get("https://news.google.com/search?{}&hl=en-US&gl=US&ceid=US%3Aen".format(user_url_search_terms)).content
  soup = BeautifulSoup(response, "html.parser")

  briefing = []

  featured = soup.find(class_='lBwEZb BL5WZb xP6mwf').findAll('div',attrs={'jscontroller':'d0DtYd'})
  for feature in featured:
    feature_row = {}
    feature_article = feature.find('article').find(class_='ZulkBc qNiaOd')
    feature_row['title'] = feature_article.span.text
    feature_row['url'] = 'https://news.google.com'+feature_article.a['href'][1:]
    feature_row['first_lines'] = feature_article.find(class_='HO8did Baotjf').text
    feature_row['source'] = feature.find(class_='QmrVtf kybdz').find('div',attrs={'class':'PNwZO zhsNkd'}).text
    feature_rawtime = feature.find('time')['datetime'].split(': ')[1]
    feature_row['time'] = datetime.datetime.fromtimestamp(int(feature_rawtime)).strftime('%Y-%m-%d %H:%M:%S')
    briefing.append(feature_row)

  articles = soup.find(class_='lBwEZb BL5WZb xP6mwf').findAll('div',attrs={'jsmodel':'zT6vwb'})
  for article in articles:
    article_row = {}
    article_row['title'] = article.find('a',attrs={'class':'ipQwMb Q7tWef'}).span.text
    article_row['url'] = 'https://news.google.com'+article.find('a',attrs={'class':'ipQwMb Q7tWef'})['href'][1:]
    article_row['first_lines'] = article.find('p').text
    article_row['source'] = article.find(class_='KbnJ8').text
    article_rawtime = re.findall(r'[\d]+', article.find('time')['datetime'].split(': ')[1])[0]
    article_row['time'] = datetime.datetime.fromtimestamp(int(article_rawtime)).strftime('%Y-%m-%d %H:%M:%S')
    briefing.append(article_row)
      
  df = pd.DataFrame(briefing)
  right_now = datetime.datetime.now()
  date_string_mail = right_now.strftime("%-I %p")
  pd.set_option('display.max_colwidth', -1)



  requests.post(
  "https://api.mailgun.net/v3/sandbox.mailgun.org/messages",
  auth=("api", "api"),
  data={"from": "Newsletter Delivery Service <postmaster@sandbox.mailgun.org>",
        "to": "<{}>".format(user_email),
        "subject": "{} News Briefing on {}".format(date_string_mail, user_topic),
        "html": df.to_html()})


   

  return render_template("immediate.html", result = result)

























# THE NEW SUBMIT BUTTON
# CALLED SUBSCRIBE

@app.route('/result', methods = ["POST", "GET"])
def result():

  if request.method == "POST":
    result = request.form


  # saving user info to variables
  user_info_list = list(result.items())
  user_name = str(user_info_list[0][1])
  user_email = str(user_info_list[1][1])

  user_topic = str(user_info_list[2][1])
  user_search_params = {'q': user_topic}
  user_url_search_terms = urllib.parse.urlencode(user_search_params)
  
  user_time = str(user_info_list[3][1])

  user_dataframe = pd.DataFrame(columns=['user_name', 'user_email', 'user_topic', 'user_time'])
  user_dataframe1 = pd.DataFrame([[user_name, user_email, user_topic, user_time]], columns=list(user_dataframe.columns))
  user_dataframe = user_dataframe.append(user_dataframe1)


  if os.environ.get('DATABASE_URL'):
    DATABASE_URL = os.environ.get('DATABASE_URL')
    conn = create_engine(DATABASE_URL)
  else:
    DATABASE_URL = "postgres://dbycbwdngelzjp:6769e3b8027bed07cc33198fb12db69330502f5788d8578284c7fcde25dca1e3@ec2-54-235-133-42.compute-1.amazonaws.com:5432/deeersqn3s60p0"
    conn = create_engine(DATABASE_URL)

  user_dataframe.to_sql('user_info', conn, if_exists='append')

  return render_template("result.html", result = result)






















# THIS IS THE SUBSCRIBE BUTTON
# NOW OBSOLETE

@app.route('/send_news', methods = ["POST", "GET"])
def send_newsletter():

  if request.method == "POST":
    result = request.form


  # saving user info to variables
  user_info_list = list(result.items())
  user_name = str(user_info_list[0][1])
  user_email = str(user_info_list[1][1])

  user_topic = str(user_info_list[2][1])
  user_search_params = {'q': user_topic}
  user_url_search_terms = urllib.parse.urlencode(user_search_params)
  
  user_time = str(user_info_list[3][1])

  user_dataframe = pd.DataFrame(columns=['user_name', 'user_email', 'user_topic', 'user_time'])
  user_dataframe1 = pd.DataFrame([[user_name, user_email, user_topic, user_time]], columns=list(user_dataframe.columns))
  user_dataframe = user_dataframe.append(user_dataframe1)


  if os.environ.get('DATABASE_URL'):
    DATABASE_URL = os.environ.get('DATABASE_URL')
    conn = create_engine(DATABASE_URL)
  else:
    DATABASE_URL = "postgres://dbycbwdngelzjp:6769e3b8027bed07cc33198fb12db69330502f5788d8578284c7fcde25dca1e3@ec2-54-235-133-42.compute-1.amazonaws.com:5432/deeersqn3s60p0"
    conn = create_engine(DATABASE_URL)

  user_dataframe.to_sql('user_info', conn, if_exists='append')

  return "nothing"









  




# @app.route("/earthquakes")
# def earthquakes():
#   cur = get_db().cursor(cursor_factory=RealDictCursor)
#   cur.execute('SELECT * FROM earthquakes;')
#   results = cur.fetchall()
#   # results = []
#   return jsonify(results)














if __name__ == '__main__':
  app.run(debug=True)
