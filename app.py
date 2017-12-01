"""Dash Charts Demo."""

from datetime import datetime as dt
from io import StringIO
import requests
import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
# from pandas_datareader import data as web
from pandas.io.common import urlencode
import pandas as pd


app = dash.Dash(__name__)
server = app.server


def populate():
    """Get the 2 columns of data from the CSV file and return an array of labels and values."""
    csv_data = pd.read_csv('data/companylist.csv', usecols=['Symbol', 'Name'])
    csv_data = csv_data.sort_values(csv_data.columns[0])
    opts = []
    for record in csv_data.to_dict('records'):
        opts.append({'label': record['Name'] + ' ' + record['Symbol'], 'value': record['Symbol']})
    return opts


app.layout = html.Div([
    html.H1([
        html.A('Dash', href="https://plot.ly/products/dash/",
               target="_blank", style={'float': 'left'}),
        html.P(': A web application framework for Python.')
    ]),
    html.H3('NASDAQ Stock Tickers', style={'clear': 'both'}),
    dcc.Dropdown(
        id='my-dropdown',
        options=populate(),
        value='AAPL'
    ),
    dcc.Graph(id='my-graph')
])


@app.callback(Output('my-graph', 'figure'), [Input('my-dropdown', 'value')])
def update_graph(selected_dropdown_value):
    """Update graph with new data of selected company."""
    # df = web.DataReader(
    #    selected_dropdown_value, data_source='google',
    #    start=dt(2017, 1, 1), end=dt.now())

    # fix for broken data reader.
    BASE = 'http://finance.google.com/finance/historical'

    def get_params(symbol, start, end):
        params = {
            'q': symbol,
            'startdate': start.strftime('%Y/%m/%d'),
            'enddate': end.strftime('%Y/%m/%d'),
            'output': "csv"
        }
        return params

    def build_url(symbol, start, end):
        params = get_params(symbol, start, end)
        return BASE + '?' + urlencode(params)

    start = dt(2017, 1, 1)
    end = dt.now()
    sym = selected_dropdown_value
    url = build_url(sym, start, end)

    data = requests.get(url).text
    data = pd.read_csv(StringIO(data), index_col='Date', parse_dates=True)

    return {
        'data': [{
            'x': data.index,
            'y': data['Close']
        }]
    }


if __name__ == '__main__':
    app.run_server()
