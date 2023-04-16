import eikon as ek
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.graph_objects as go 
from plotly.subplots import make_subplots
from numerize import numerize

# Eikon API key
ek.set_app_key('04c0e3f661bd49348d69c3aabedb8c0108cfd1e2')

# Retrieve stock data
def get_stock_data(symbol, start_date, end_date):
    df, err = ek.get_data(symbol, [
            'TR.F.EVToEBIT','TR.F.EVToEBITDA','TR.EVToSales(1D)','TR.FwdPtoEPSSmartEst','TR.PriceToBVPerShare',
            'TR.PriceToCFPerShare','TR.PriceClose/TR.FreeOperatingCashFlowperShareAvgDilutedSharesOut', 'TR.Volatility260D/100',
            'TR.ReturnonAvgTotEqtyPctNetIncomeBeforeExtraItems/100', 'TR.ROATotalAssetsPercent/100','TR.GrossMargin/100',
            'TR.NetIncome/TR.Revenue','TR.LTDebtToTtlEqtyPct/100','TR.LTDebtToTtlCapitalPct/100','TR.TimesInterestEarned',
            'TR.BusinessSummary','TR.BusinessSummary','TR.OrgFoundedYear','TR.CompanyNumEmploy','TR.OrganizationWebsite',
            'TR.Revenue','TR.CompanyMarketCap','TR.RepNetProfitMean','PERATIO','TR.PriceToSalesPerShare',
            'TR.F.COGSTot','TR.DividendYield','TR.F.DivPayoutRatioPct/100', 'TR.ClosePrice.Date','TR.ClosePrice'
            ],
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
    Output('fundamental-graph', 'figure'),
    [Input('submit-button', 'n_clicks')],
    [dash.dependencies.State('symbol-input', 'value'),
     dash.dependencies.State('start-date-input', 'value'),
     dash.dependencies.State('end-date-input', 'value')]
)
def update_graph(n_clicks, symbol, start_date, end_date):
    df = get_stock_data(symbol, start_date, end_date)
    return equity_graph(df)

# All Graphs:
# Equity Graph stylisation
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
# Basic Fundamentals Graph
def bar_fig(market_cap,revenue,earnings,pe_ratio,ps_ratio):
    fig = make_subplots(rows=1,cols=2,column_widths=[0.7, 0.3])
    fig.add_trace(go.Bar(
        x=[earnings,revenue,market_cap],
        y=['Earnings','Revenue','Market Cap'],
        orientation='h',
        marker_color = ['green','blue','navy'],
        width = [1,1,1],
        showlegend = False,
        text = [
            f'Earnings {numerize.numerize(earnings)}',
            f'Revenue {numerize.numerize(revenue)}',
            f'Market Cap {numerize.numerize(market_cap)}'
            ]
        ),row=1,col=1
    )
    fig.update_traces(
        textfont_size=12,
        textangle=0,
        textposition="outside",
        cliponaxis=False
        )
    fig.update_layout(
        plot_bgcolor="white",
        bargap=0,
        height=400,
        width=700
        )
    fig.update_xaxes(
        showticklabels=False
        )
    fig.update_yaxes(
        showticklabels=False
        )
    fig.add_trace(
        go.Scatter(
            x=[0,100],
            y=[0,100],
            mode='markers',
            marker=dict(opacity=0),
            showlegend=False
            ),
        row=1,
        col=2
        )
    fig.add_annotation(
        x=25,
        y=60,
        text=f'{pe_ratio}x',
        font=dict(size=30,color='navy'),
        showarrow=False,
        arrowhead=1,
        row=1,
        col=2
        )
    fig.add_annotation(
        x=100,
        y=60,
        text=f'{ps_ratio}x',
        font=dict(size=30,color='navy'),
        showarrow=False,
        arrowhead=1,
        row=1,
        col=2
        )
    fig.add_annotation(
        x=25,
        y=45,
        text='PE Ratio',
        font=dict(size=18,color='navy'),
        showarrow=False,
        arrowhead=1,
        row=1,
        col=2
        )
    fig.add_annotation(
        x=100,
        y=45,
        text='PS Ratio',
        font=dict(size=18,color='navy'),
        showarrow=False,
        arrowhead=1,
        row=1,
        col=2
        )
    return fig


# Run app
if __name__ == '__main__':
    app.run_server(debug=True)
