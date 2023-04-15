import eikon as ek
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import pandas as pd
# Eikon API key
ek.set_app_key('04c0e3f661bd49348d69c3aabedb8c0108cfd1e2')

# Retrieve stock data
def get_stock_data(symbol, start_date, end_date):
    df, err = ek.get_data(symbol, ['TR.ClosePrice.Date', 'TR.ClosePrice'],
                          {'SDate': start_date, 'EDate': end_date})
    return df

# Initialize Dash app
app = dash.Dash(__name__)

# Define app layout
app.layout = html.Div([
    html.H1('Eikon Stock Data'),
    html.Div([
        html.Label('Enter Stock Symbol:'),
        dcc.Input(id='symbol-input', type='text', value='AAPL.O'),
        html.Label('Start Date (YYYY-MM-DD):'),
        dcc.Input(id='start-date-input', type='text', value='2021-01-01'),
        html.Label('End Date (YYYY-MM-DD):'),
        dcc.Input(id='end-date-input', type='text', value='2021-12-31'),
        html.Button('Submit', id='submit-button', n_clicks=0),
    ]),
    dcc.Graph(id='stock-graph'),
])

# Define app callbacks
@app.callback(
    Output('stock-graph', 'figure'),
    [Input('submit-button', 'n_clicks')],
    [dash.dependencies.State('symbol-input', 'value'),
     dash.dependencies.State('start-date-input', 'value'),
     dash.dependencies.State('end-date-input', 'value')]
)
def update_graph(n_clicks, symbol, start_date, end_date):
    df = get_stock_data(symbol, start_date, end_date)
    return {
        'data': [{
            'x': df['Date'],
            'y': df['Close Price'],
            'type': 'line',
            'name': symbol
        }],
        'layout': {
            'title': f'{symbol} Closing Prices'
        }
    }

# Run app
if __name__ == '__main__':
    app.run_server(debug=True)