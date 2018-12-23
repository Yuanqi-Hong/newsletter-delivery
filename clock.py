from apscheduler.schedulers.blocking import BlockingScheduler
import requests, os, datetime, re
from sqlalchemy import create_engine
from bs4 import BeautifulSoup
import pandas as pd
import urllib.parse

sched = BlockingScheduler(timezone="America/New_York")

@sched.scheduled_job('cron', day_of_week='tue', hour=17, minute=15)
def scheduled_email():
  if os.environ.get('DATABASE_URL'):
    DATABASE_URL = os.environ.get('DATABASE_URL')
    conn = create_engine(DATABASE_URL)
  else:
    DATABASE_URL = ""
    conn = create_engine(DATABASE_URL)


  user_email = pd.read_sql("SELECT user_email FROM user_info WHERE user_time='17:15'", conn)
  
  user_topic = pd.read_sql("SELECT user_topic FROM user_info WHERE user_time='17:15'", conn)
  # user_search_params = {'q': user_topic}
  # user_url_search_terms = urllib.parse.urlencode(user_search_params)

  

  user_email_v = user_email['user_email'].values[0]
  user_topic_v = user_topic['user_topic'].values[0]
  user_search_params = {'q': user_topic_v}
  user_url_search_terms = urllib.parse.urlencode(user_search_params)



  # SCRAPER

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




  # EMAIL SENDER

  requests.post(
  "https://api.mailgun.net/v3/sandbox.mailgun.org/messages",
  auth=("api", "api"),
  data={"from": "Newsletter Delivery Service <postmaster@sandbox.mailgun.org>",
        "to": "<{}>".format(user_email_v),
        "subject": "{} News Briefing on {}".format(date_string_mail, user_topic_v),
        "html": df.to_html()})










sched.start()
