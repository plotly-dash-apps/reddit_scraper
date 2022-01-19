import plotly.graph_objs as go
import requests
from bs4 import BeautifulSoup
import pandas as pd
import datetime



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
                    header=dict(values=['date', 'time', 'post'], align=['left']),
                    cells=dict(align=['left'],
                               values=[['whoa!','whoa!','whoa!'],
                                       [3,2,1],
                                       ['Slow down!','Scraping takes a sec','Try back later!']])
                 )
    fig = go.Figure([data])
    return fig




########### Functions  ######

# define a scraper function
def lovely_soup(url):
    r = requests.get(url, headers = {'User-agent': 'Agent_Smith'})
    return BeautifulSoup(r.text, 'lxml')
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

    ########### Pandas work ######
    # convert the two lists into a pandas dataframe
    df_dict={'date':dateslist, 'post':titleslist}
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
    final_df = working_df[['date', 'time', 'post']].copy()



    ########### Set up the figure ######

    data=go.Table(columnwidth = [200,200,1000],
                    header=dict(values=final_df.columns, align=['left']),
                    cells=dict(align=['left'],
                               values=[final_df['date'],
                                       final_df['time'],
                                       final_df['post'].values])
                 )
    fig = go.Figure([data])
    return fig
