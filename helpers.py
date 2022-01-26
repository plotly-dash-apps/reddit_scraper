import plotly.graph_objs as go
import requests
from bs4 import BeautifulSoup
import pandas as pd
import datetime
import lxml
import urllib.request
from fake_useragent import UserAgent

########### Set up the default figures ######

def base_fig():
    data=go.Table(columnwidth = [200,200,1000],
                    header=dict(values=['date', 'time', 'post'], align=['left']),
                    cells=dict(align=['left'],
                               values=[[1,2,3],
                                       [1,2,3],
                                       ['waiting for data','waiting for data','waiting for data']])
                 )
    fig = go.Figure([data])
    return fig

def error_fig():
    data=go.Table(columnwidth = [200,200,1000],
                    header=dict(values=['date', 'time', 'post', ], align=['left']),
                    cells=dict(align=['left'],
                               values=[['whoa!','whoa!','whoa!'],
                                       [3,2,1],
                                       ['Slow down!','Scraping takes a sec','Try back later!']])
                 )
    fig = go.Figure([data])
    return fig




########### Functions  ######

ua = UserAgent()

# import random
# user_agent_list = [
# 'Class_practice',
# 'Mozilla/5.0',
# 'Chrome/83.0.4103.97 ',
# 'Safari/537.36',
# ]
# #url = 'https://httpbin.org/headers'
# for i in range(1,4):
# #Pick a random user agent
#     user_agent = random.choice(user_agent_list)
# #Set the headers
#     headers = {'User-Agent': user_agent}

# define a scraper function
def lovely_soup(url):
#     h = {'User-Agent': ua.Chrome}
#     # r = get(u, headers=h)
    r = requests.get(url, headers = {'User-agent': 'class_practice'})
#     r = requests.get(url, headers=h)
# #    return BeautifulSoup(r.text, 'lxml')
    return BeautifulSoup(r.text, 'html')
# write a function to clean up the post
def clean_that_post(row):
    x = row.split(' (self.AskReddit)')
    return x[0]
# write a function to clean up the date
def parse_that_date(row):
    x = row.split(' ')[1:]
    y = ' '.join(x)
    z = '2020 '+ y
    return z[:20]

########### Scraping ######

def scrape_reddit():
    # apply the function to our reddit source
    url = 'https://old.reddit.com/r/AskReddit/'
    soup = lovely_soup(url)
    # create a list of titles
    titles = soup.findAll('p', {'class': 'title'})
    titleslist=[]
    for title in titles:
        titleslist.append(title.text)
    # create a list of dates
    dates = soup.findAll('time', {'class':"live-timestamp"})
    dateslist=[]
    for date in dates:
        output = str(date).split('title="')[1].split('2020')[0]
        dateslist.append(output)
    # create URL links
    parser = 'html.parser'
    resp = urllib.request.urlopen("https://old.reddit.com/r/AskReddit/")
    soup = BeautifulSoup(resp, parser, from_encoding=resp.info().get_param('charset'))
    links = soup.find_all('a', 'comments', href=True)
    linkslist = []
    for link in links:
        linkslist.append(link['href'])
    #    print(link['href'])
    df = pd.DataFrame(linkslist)
    def make_clickable(val):
        return '<a target="_blank" href="{}">{}</a>'.format(val, val)
    clickable_link = df.style.format(make_clickable)
    ########### Pandas work ######
    # convert the 3 lists into a pandas dataframe
    df_dict={'date':dateslist, 'post':titleslist, 'links':linkslist}
    working_df = pd.DataFrame(df_dict)
    pd.set_option('display.max_colwidth', 200)
    working_df['date'] = working_df['date'].str.strip()

    # apply the function
    working_df['post']=working_df['post'].apply(clean_that_post)

    # apply the date parsing function and sort the dataframe
    working_df['cleandate']=working_df['date'].apply(parse_that_date)
    working_df['UTC_date'] = pd.to_datetime(working_df['cleandate'])
    working_df.sort_values('UTC_date', inplace=True, ascending=False)
    # split into 2 date/time variables
    working_df['date']=working_df['UTC_date'].dt.date
    working_df['time']=working_df['UTC_date'].dt.time
    final_df = working_df[['date', 'time', 'post', 'links']].copy()



    ########### Set up the figure ######

    data=go.Table(columnwidth = [200,200,500,800],
                    header=dict(values=final_df.columns, align=['left']),
                    cells=dict(align=['left'],
                               values=[final_df['date'],
                                       final_df['time'],
                                       final_df['post'].values,
                                       #final_df['clickable_link'].values])
                                       final_df['links'].values])
                 )
    fig = go.Figure([data])
    return fig
