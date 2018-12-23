# import pandas as pd
# import os
# from sqlalchemy import create_engine

# df = pd.read_csv("https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/1.0_hour.csv")

# if os.environ.get('DATABASE_URL'):
#     DATABASE_URL = os.environ.get('DATABASE_URL')
#     conn = create_engine(DATABASE_URL)
# else:
#     DATABASE_URL = "postgres://dbycbwdngelzjp:6769e3b8027bed07cc33198fb12db69330502f5788d8578284c7fcde25dca1e3@ec2-54-235-133-42.compute-1.amazonaws.com:5432/deeersqn3s60p0"
#     conn = create_engine(DATABASE_URL)

# df.to_sql('earthquakes', conn, if_exists='append')
# pd.read_sql("SELECT COUNT(*) FROM earthquakes", conn)
# print(pd.read_sql("SELECT COUNT(*) FROM earthquakes", conn))

# Generating auto-emails on China-related news from Google News
# BONUS: presenting the content not as an CSV attachment but as the body of email

# from bs4 import BeautifulSoup
# import requests
# import datetime
# import re
# import pandas as pd

# response = requests.get("https://news.google.com/search?q=China&hl=en-US&gl=US&ceid=US%3Aen").content
# soup = BeautifulSoup(response, "html.parser")

# briefing = []

# featured = soup.find(class_='lBwEZb BL5WZb xP6mwf').findAll('div',attrs={'jscontroller':'d0DtYd'})
# for feature in featured:
#     feature_row = {}
#     feature_article = feature.find('article').find(class_='ZulkBc qNiaOd')
#     feature_row['title'] = feature_article.span.text
#     feature_row['url'] = 'https://news.google.com'+feature_article.a['href'][1:]
#     feature_row['first_lines'] = feature_article.find(class_='HO8did Baotjf').text
#     feature_row['source'] = feature.find(class_='QmrVtf kybdz').find('div',attrs={'class':'PNwZO zhsNkd'}).text
#     feature_rawtime = feature.find('time')['datetime'].split(': ')[1]
#     feature_row['time'] = datetime.datetime.fromtimestamp(int(feature_rawtime)).strftime('%Y-%m-%d %H:%M:%S')
#     briefing.append(feature_row)

# articles = soup.find(class_='lBwEZb BL5WZb xP6mwf').findAll('div',attrs={'jsmodel':'zT6vwb'})
# for article in articles:
#     article_row = {}
#     article_row['title'] = article.find('a',attrs={'class':'ipQwMb Q7tWef'}).span.text
#     article_row['url'] = 'https://news.google.com'+article.find('a',attrs={'class':'ipQwMb Q7tWef'})['href'][1:]
#     article_row['first_lines'] = article.find('p').text
#     article_row['source'] = article.find(class_='KbnJ8').text
#     article_rawtime = re.findall(r'[\d]+', article.find('time')['datetime'].split(': ')[1])[0]
#     article_row['time'] = datetime.datetime.fromtimestamp(int(article_rawtime)).strftime('%Y-%m-%d %H:%M:%S')
#     briefing.append(article_row)
    
# df = pd.DataFrame(briefing)
# right_now = datetime.datetime.now()
# date_string_mail = right_now.strftime("%-I %p")
# pd.set_option('display.max_colwidth', -1)

# requests.post(
#         "https://api.mailgun.net/v3/MY_SANDBOX_DOMAIN/messages",
#         auth=("api", "api"),
#         data={"from": "Edward Hong <mailgun@MY_SANDBOX_DOMAIN>",
#               "to": ["{} Edward.YSHF@gmail.com".format(processed_text)],
#               "subject": "{} China News Briefing".format(date_string_mail),
#               "html": df.to_html()})