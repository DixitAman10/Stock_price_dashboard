# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import dash
import dash_auth
from dash import dcc
from dash import html
from dash.dependencies import Input, Output, State
import pandas_datareader.data as web
from datetime import datetime
import os
# import pandas
import pandas as pd

#from datetime import datetime
#start = datetime(2016, 9, 1)
#end = datetime(2018, 9, 1)
#f = web.DataReader('F', 'iex', start, end)

USERNAME_PASSWORD_PAIRS =  [['username','password'],['Stock','Price']]

app = dash.Dash()
auth = dash_auth.BasicAuth(app,USERNAME_PASSWORD_PAIRS)
os.environ['alphavantage_api_key'] = "ZEQB2KKQ5EG6T1KQ"

# read a .csv file, make a dataframe, and build a list of Dropdown options

nsdq = pd.read_csv('E://nasdaq.csv')
nsdq.set_index('Symbol', inplace=True)
options = []
for tic in nsdq.index:
    options.append({'label':'{}'.format(tic,nsdq.loc[tic]['Name']), 'value':tic})

app.layout = html.Div([
    html.H1('Stock Ticker Dashboard'),
    html.Div([
        html.H3('Select stock symbols:', style={'paddingRight':'30px'}),
        # replace dcc.Input with dcc.Options, set options=options
        dcc.Dropdown(
            id='my_ticker_symbol',
            options=options,
            value='TSLA',
            multi=True
         )

    # widen the Div to fit multiple inputs
    ], style={'display':'inline-block', 'verticalAlign':'top', 'width':'30%'}),
    html.Div([
        html.H3('Select start and end dates:'),
        dcc.DatePickerRange(
            id='my_date_picker',
            min_date_allowed=datetime(2000, 1, 1),
            max_date_allowed=datetime.today(),
            start_date=datetime(2022, 1, 1),
            end_date=datetime.today()
        )
    ], style={'display':'inline-block'}),
    html.Div([
        html.Button(
            id='submit-button',
            n_clicks=0,
            children='Submit',
            style={'fontSize':24, 'marginLeft':'30px'}
        ),
    ], style={'display':'inline-block'}),
    dcc.Graph(
        id='my_graph',
        figure={
            'data': [
                {'x': [1,2], 'y': [3,1]}
            ]
        }
    )
])
@app.callback(
    Output('my_graph', 'figure'),
    [Input('submit-button', 'n_clicks')],
    [State('my_ticker_symbol', 'value'),
    State('my_date_picker', 'start_date'),
    State('my_date_picker', 'end_date')])
def update_graph(n_clicks, stock_ticker, start_date, end_date):
    start = datetime.strptime(start_date[:10], '%Y-%m-%d')
    end = datetime.strptime(end_date[:10], '%Y-%m-%d')
    # since stock_ticker is now a list of symbols, create a list of traces
    traces = []
    for tic in stock_ticker:
        df = web.DataReader(tic, "av-weekly", start, end, api_key=os.getenv('alphavantage_api_key'))
        traces.append({'x':df.index, 'y': df.close, 'name':tic})
    fig = {
        # set data equal to traces
        'data': traces,
        # use string formatting to include all symbols in the chart title
        'layout': {'title':', '.join(stock_ticker)+' Closing Prices'}
    }
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)






# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
