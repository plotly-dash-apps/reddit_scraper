
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import plotly.graph_objs as go
from helpers import *

########### Define a few variables ######

tabtitle = 'Reddit Webscraper'
sourceurl = 'https://old.reddit.com/r/AskReddit/'
githublink = 'https://git.generalassemb.ly/allenchua/524-reddit-webscraper/'

########### Initiate the app
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
app.title=tabtitle

########### Layout ###########

app.layout = html.Div(children=[
    html.H1('Webscraping posts from reddit (w/ URLs)'),
    # Dropdowns
    html.Div(children=[
        html.Button('Scrape Now!', id='submit-val', n_clicks=0),
        html.Div(id='message'),
        dcc.Graph(id='figure-1'),
    ], className='twelve columns'),

    # Footer
    html.Br(),
    html.Br(),
    html.A('Code on Github', href=githublink),
    html.Br(),
    html.A("Data Source", href=sourceurl),
    ]
)

########### Callback ###########

@app.callback(
    [Output('message', 'children'),
    Output('figure-1', 'figure')],
    [Input('submit-val', 'n_clicks')],
    )
def update_output(n_clicks):
    if n_clicks==0:
        message = f"Click the button"
        return message, base_fig()
    elif n_clicks==1:
        message = f"You've clicked that button {n_clicks} time!"
        return message, scrape_reddit()
    elif (n_clicks>1) & (n_clicks<5):
        message = f"You've clicked that button {n_clicks} times!"
        return message, error_fig()
    else:
        message = f"Seriously, stop clicking the button. You've clicked it {n_clicks} times."
        return message, error_fig()


############ Deploy
if __name__ == '__main__':
    app.run_server(debug=True)
