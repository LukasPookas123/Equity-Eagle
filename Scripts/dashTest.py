import eikon as ek
from dash import Dash, Input, Output, dcc, html
import pandas as pd
import plotly.graph_objects as go 
from plotly.subplots import make_subplots
from numerize import numerize
from bs4 import BeautifulSoup
from textblob import TextBlob
import numpy as np

# Eikon API key
louis_key = '04c0e3f661bd49348d69c3aabedb8c0108cfd1e2'
luke_key = '374e43f5a0644568896478f5e6ba69d050467a4d'
ek.set_app_key(luke_key)

# Retrieve stock data
def get_stock_data(symbol):
    df, err = ek.get_data(symbol, [
                'TR.GrossMargin/100','TR.F.OthNonOpIncExpnTot(Period=FY0)','TR.Revenue','TR.CompanyMarketCap',
                'TR.RepNetProfitMean','PERATIO','TR.PriceToSalesPerShare', 'TR.NetIncome', 'TR.GrossIncomeMean(Period=FY1)','TR.F.COGSInclOpMaintUtilTot(Period=FY0)',
                ])
    df_date = ek.get_timeseries(symbol,'CLOSE',interval='daily', start_date='2019-01-01')
    df_news = ek.get_news_headlines('PresetTopic:[Significant News: All] AND R:{} AND Language:LEN'.format(symbol), count=1)

    return df, df_date, df_news

external_stylesheets = [
    {
        "href": (
            "https://fonts.googleapis.com/css2?"
            "family=Lato:wght@400;700&display=swap"
        ),
        "rel": "stylesheet",
    },
]

# Initialise app
app = Dash(__name__, external_stylesheets=external_stylesheets)
app.title = "Fundamental Analysis"

name_df = pd.read_csv("C:/Users/luke-/Documents/My Stuff/1 - PY PROJECTS/Equity-Eagle/Scripts/AllStockNames.csv")

names = name_df['Updated at 18:21:34'].tolist()

# Define app layout
app.layout = html.Div(
    children=[
        html.Div(
            children=[
                html.H1(
                    children="Fundamental Analysis", className="header-title"
                ),
                html.P(
                    children=(
                        "Analyze extracted company data from Refinitiv"
                        " in the form of various charts"
                    ),
                    className="header-description",
                ),
            ],
            className="header",
        ),
        html.Div(
            children=[
                html.Div(
                    children=[
                        html.Div(children="Name", className="menu-title"),
                        dcc.Dropdown(
                            id="name-filter",
                            options=[
                                {"label": name, "value": name}
                                for name in names
                            ],
                            value="AAPL.O",
                            clearable=False,
                            className="dropdown",
                        ),
                    ]
                ),
            ],
            className="menu",
        ),
        html.Div(
            children=[
                html.Div(
                    children=dcc.Graph(
                        id="graph-one",
                        config={"displayModeBar": False},
                    ),
                    className="card",
                ),
            ],
            className="wrapper",
        ),
        html.Div(
            children=[
                html.Div(
                    children=dcc.Graph(
                        id="graph-two",
                        config={"displayModeBar": False},
                    ),
                    className="card",
                ),
            ],
            className="wrapper",
        ),
        html.Div(
            children=[
                html.Div(
                    children=dcc.Graph(
                        id="graph-three",
                        config={"displayModeBar": False},
                    ),
                    className="card",
                ),
            ],
            className="wrapper",
        ),
        html.Div(
            children=[
                html.Div(
                    children=[
                        html.Span(id="news"),
                        #html.Img(id="sentiment"),
                        html.Span(id="score"),
                    ],
                    className="card",
                ),
            ],
            className="wrapper",
        ),
    ]
)

# Define app callbacks
@app.callback(
    Output('graph-one', 'figure'),
    Output('graph-two', 'figure'),
    Output('graph-three', 'figure'),
    Output('news', 'children'),
    Output('score', 'children'),
    #Output('sentiment', 'src'),
    Input("name-filter", "value"),
)
def update_graph(symbol):
    df, df_date, df_news = get_stock_data(symbol)

    '''
    Callback function

    Input:
        symbol: string

    Output:
        graph-one
        graph-two
        graph-three
        news
        sentiment
        score

    Code below extracts sentiment using TextBlob and BeautifulSoup (NLP) - very cool.
    Kept some code commented out because Louis spent a lot of time on it and I don't want to delete it (GitHub Copilot autofilled that).
    '''

    #df['HTML'] = df['storyId'].apply(ek.get_news_story) #create col with article html
    # #get sentiments and objectivity
    # df['Polarity'] = np.nan
    # df['Subjectivity'] = np.nan
    df_news['Score'] = np.nan

    for idx, storyId in enumerate(df['storyId'].values):
        newsText = ek.get_news_story(storyId) #get the news story
        if newsText:
            soup = BeautifulSoup(newsText,"lxml") #create a BeautifulSoup object from our HTML news article
            sentA = TextBlob(soup.get_text()) #pass the text only article to TextBlob to anaylse
            # df['Polarity'].iloc[idx] = sentA.sentiment.polarity #write sentiment polarity back to df
            # df['Subjectivity'].iloc[idx] = sentA.sentiment.subjectivity #write sentiment subjectivity score back to df
            if sentA.sentiment.polarity >= 0.05: # attribute bucket to sentiment polartiy
                score = 'positive'
            elif  -.05 < sentA.sentiment.polarity < 0.05:
                score = 'neutral'
            else:
                score = 'negative'
            df_news['Score'].iloc[idx] = score #write score back to df

    return equity_graph(df_date.index, df_date['CLOSE']), \
           bar_fig(df['Company Market Cap'][0],df['Revenue'][0],df['Net Income Reported - Mean'][0], \
                   df['PERATIO'][0],df['Price To Sales Per Share (Daily Time Series Ratio)'][0]), \
           income_statement_bar(df['Revenue'][0],df['Cost of Revenue incl Operation & Maintenance (Utility) Total'][0], \
                                df['Gross Income - Mean'][0],df['Net Income Reported - Mean'][0],df['Net Income Reported - Mean'][0]), \
           news(df_news), score_display(sentA.sentiment.polarity)#, sentiment(df_news)

# All Graphs:
# Equity Graph stylisation
def equity_graph(dates, close_prices):
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x = dates,
            y = close_prices,
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
            f'Earnings {numerize.numerize(earnings.item())}',
            f'Revenue {numerize.numerize(revenue.item())}',
            f'Market Cap {numerize.numerize(market_cap.item())}'
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
        x=24,
        y=20,
        text=f'{round(pe_ratio, 1)}x',
        font=dict(size=30,color='navy'),
        showarrow=False,
        arrowhead=1,
        row=1,
        col=2
        )
    fig.add_annotation(
        x=24,
        y=60,
        text=f'{round(ps_ratio, 1)}x',
        font=dict(size=30,color='navy'),
        showarrow=False,
        arrowhead=1,
        row=1,
        col=2
        )
    fig.add_annotation(
        x=24,
        y=10,
        text='PE Ratio',
        font=dict(size=18,color='navy'),
        showarrow=False,
        arrowhead=1,
        row=1,
        col=2
        )
    fig.add_annotation(
        x=24,
        y=50,
        text='PS Ratio',
        font=dict(size=18,color='navy'),
        showarrow=False,
        arrowhead=1,
        row=1,
        col=2
        )
    return fig

# Income Statement Graph
def income_statement_bar(revenue,cost_of_sales,gross_profit,net_income,earnings):
    financials=['Revenue', 'Cost of Sales', 'Gross Profit','Other Expenses','Net Income']
    other_expenses = gross_profit - earnings
    fig = go.Figure()
    fig.add_trace(
        go.Bar(
            x=financials,
            y=[revenue,gross_profit,gross_profit,net_income,net_income],
            showlegend=False,
            marker_color=['navy','white','green','white','aquamarine'],
            text=[f'${numerize.numerize(revenue.item())}','',f'${numerize.numerize(gross_profit.item())}','',f'${numerize.numerize(net_income.item())}']
            )
        )
    fig.add_trace(
        go.Bar(
            x=financials,
            y=[0,revenue-gross_profit,0,other_expenses,0],
            showlegend=False,
            marker_color=['crimson','crimson','red','crimson','red'],
            text=['',f'${numerize.numerize(cost_of_sales.item())}','',f'${numerize.numerize(other_expenses.item())}','']
            )
        )
    fig.update_layout(
        plot_bgcolor="white",
        barmode='stack',
        bargap=0,
        xaxis = dict(tickfont = dict(size=18))
        )
    fig.update_traces(textposition="outside",)
    fig.update_yaxes(showticklabels=False)
    fig.update_yaxes(showline=False)
    fig.update_layout(xaxis = dict(tickfont = dict(size=18)))
    fig.update_yaxes()
    return fig

def news(df):
    return df['text'][0]

# def sentiment(df):
#     for i in range(len(df.index)):
#         if df['Score'][i] == 'positive':
#             return "URL FOR POSITIVE IMAGE"
#         elif df['Score'][i] == 'negative':
#             return "URL FOR NEGATIVE IMAGE"
#         else:
#             return "URL FOR NEUTRAL IMAGE"

def score_display(number):
    return number

# Run app
if __name__ == '__main__':
    app.run_server(debug=True)
