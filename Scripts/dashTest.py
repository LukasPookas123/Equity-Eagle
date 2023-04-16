import eikon as ek
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.graph_objects as go 

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
        dcc.Input(id='start-date-input', type='text', value='2019-01-01'),
        html.Label('End Date (YYYY-MM-DD):'),
        dcc.Input(id='end-date-input', type='text', value='2022-12-31'),
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
    return equity_graph(df)

# All Graphs:
#Equity Graph stylisation
def equity_graph(df):
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x = df['Date'],
            y = df['Close Price'],
            mode = 'lines',
            line_color ='navy'
            )
        )
    fig.update_yaxes(
        showline=True,
        linewidth=2,
        linecolor='navy',
        tickprefix="US$",
        autorange=True
        )
    fig.update_xaxes(
        showline=True,
        linewidth=2,
        linecolor='navy',
        showspikes=True,
        spikecolor="navy",
        spikesnap="cursor",
        spikemode="across",
        spikedash="solid",
        spikethickness=2
        )
    fig.update_xaxes(
        rangeslider_visible=False,
        rangeselector=dict(
            buttons=list([
                dict(
                    count=1,
                    label="1m",
                    step="month",
                    stepmode="backward"
                    ),
                dict(
                    count=6,
                    label="6m",
                    step="month",
                    stepmode="backward"
                    ),
                dict(
                    count=1,
                    label="YTD",
                    step="year",
                    stepmode="todate"
                    ),
                dict(
                    count=1,
                    label="1y",
                    step="year",
                    stepmode="backward"
                    ),
                dict(
                    count=2,
                    label="2y",
                    step="year",
                    stepmode="backward"
                    ),
                dict(
                    count=5,
                    label="5y",
                    step="year",
                    stepmode="backward"
                    ),
                dict(step="all")
            ])
        )
    )
    fig.update_layout(
        xaxis_rangeselector_font_color='white',
        xaxis_rangeselector_activecolor='grey',
        xaxis_rangeselector_bgcolor='navy',
        hovermode='x',
        plot_bgcolor="white"
        )
    return fig

# Run app
if __name__ == '__main__':
    app.run_server(debug=True)