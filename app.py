import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
from pandas_datareader import data as web
import pandas as pd
from datetime import datetime as dt

app = dash.Dash(__name__)
server = app.server


def populate():
    csv_data = pd.read_csv('data/companylist.csv', usecols=['Symbol', 'Name'])
    csv_data = csv_data.sort_values(csv_data.columns[0])
    opts = []
    for x in csv_data.to_dict('records'):
        opts.append({'label': x['Name'], 'value': x['Symbol']})
    return opts


# {'label': 'Apple', 'value': 'AAPL'},
# {'label': 'Adobe', 'value': 'ADBE'},
# {'label': 'Coke', 'value': 'COKE'},
# {'label': 'Exxon', 'value': 'XOM'},
# {'label': 'Microsoft', 'value': 'MSFT'},
# {'label': 'Tesla', 'value': 'TSLA'}


app.layout = html.Div([
    html.H1([
        html.A('Dash', href="https://plot.ly/products/dash/", target="_blank", style={'float': 'left'}),
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
    df = web.DataReader(
        selected_dropdown_value, data_source='google',
        start=dt(2017, 1, 1), end=dt.now())
    return {
        'data': [{
            'x': df.index,
            'y': df.Close
        }]
    }


if __name__ == '__main__':
    app.run_server()
