import streamlit as st
import pandas as pd 
import plotly.graph_objects as go 
import streamlit as st
import yfinance as yf
import datetime as dt
from plotly.subplots import make_subplots
from numerize import numerize
import os
import pandas as pd
import datetime as dt
import os
from bs4 import BeautifulSoup
from textblob import TextBlob
import eikon as ek
import numpy as np


def equity_graph(df):
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x = df.index,
            y = df['Close'],
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

def income_statement_bar(revenue,cost_of_sales,gross_profit,other_expenses,net_income):
    financials=['Revenue', 'Cost of Sales', 'Gross Profit','Other Expenses','Net Income']
    fig = go.Figure()
    fig.add_trace(
        go.Bar(
            x=financials,
            y=[revenue,gross_profit,gross_profit,net_income,net_income],
            showlegend=False,
            marker_color=['navy','white','green','white','aquamarine'],
            text=[f'${numerize.numerize(revenue)}','',f'${numerize.numerize(gross_profit)}','',f'${numerize.numerize(net_income)}']
            )
        )
    fig.add_trace(
        go.Bar(
            x=financials,
            y=[0,cost_of_sales,0,other_expenses,0],
            showlegend=False,
            marker_color=['crimson','crimson','red','crimson','red'],
            text=['',f'${numerize.numerize(cost_of_sales)}','',f'${numerize.numerize(other_expenses)}','']
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

def peer_PE_bar():
        x_plot = [20, 14, 23, 12, 24]
        y_plot = ['giraffes', 'orangutans', 'monkeys', 'animal1', 'animal2']

        fig = go.Figure()
        fig.add_trace(go.Bar(
            y=y_plot,
            x=x_plot,
            orientation='h',
            name='SF Zoo',
            marker=dict(
                color='rgba(58, 71, 80, 0.15)',
                line=dict(color='rgba(58, 71, 80, 1.0)', width=3)
            ),
            text = [
                f'{x_plot[4]}',
                f'{x_plot[3]}',
                f'{x_plot[2]}',
                f'{x_plot[1]}',
                f'{x_plot[0]}',
                ]
            )
        )

        fig.update_layout(barmode='stack', xaxis_title="Price to Earnings Ratio", shapes=[
            dict(
            type= 'line',
            yref= 'paper', y0= 0, y1= 1,
            xref= 'x', x0= sum(x_plot)/len(x_plot), x1= sum(x_plot)/len(x_plot)
            )
        ])

        fig.add_annotation(x=(sum(x_plot)/len(x_plot))-1,
                           y=5,
                           text=f'Peer Average {sum(x_plot)/len(x_plot)}x',
                           ax=0,
                           ay=0,
                           font=dict(size=15, color="black"))
        
        fig.update_traces (
            textfont_size=12,
            textangle=0,
            textposition="outside",
            cliponaxis=False
        )
        return fig

def volatility(ticker):
    dataPath = os.path.abspath(os.path.join(os.path.dirname((os.path.curdir.__dir__()[0])), '..', 'Data'))
    fundDF = pd.read_csv(dataPath+'\\{}\\Fundamentals.csv'.format(ticker))
    pDF = pd.read_csv(dataPath+'\\{}\\Peers.csv'.format(ticker))
    volAvg = pDF['TR.VOLATILITY260D/100'].mean()
    volAsset = fundDF['TR.VOLATILITY260D/100'][0]
    if (volAvg>volAsset):
        high = volAvg
    else:
        high = volAsset

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=[volAsset,volAvg], y=[0,0], mode='markers+text', marker_size=30, text=[ticker,'Industry'], textposition='top center', marker_symbol = 'star-diamond',marker_color="midnightblue",
    ))
    fig.add_annotation(x=0.025
        , y=0
        , text=f'Low'
        , showarrow=True
        , arrowhead=1
        , arrowsize=1
        , arrowwidth=2
        , arrowcolor="#636363"
        , ax=0
        , ay=0
        , font=dict(size=12, color="white", family="Courier New, monospace")
        , align="left"
        , bordercolor='black'
        , borderwidth=2
        , bgcolor="black"
        , opacity=1)
    fig.add_annotation(x=high+0.1
        , y=0
        , text=f'High'
        , showarrow=True
        , arrowhead=1
        , arrowsize=1
        , arrowwidth=2
        , arrowcolor="#636363"
        , ax=0
        , ay=0
        , font=dict(size=12, color="white", family="Courier New, monospace")
        , align="left"
        , bordercolor='black'
        , borderwidth=2
        , bgcolor="black"
        , opacity=1)
    fig.update_xaxes(showgrid=False,)
    fig.update_yaxes(showgrid=False,
                    zeroline=True, zerolinecolor='green', zerolinewidth=20,
                    showticklabels=False, range=[0,0])
    fig.update_layout(height=500, plot_bgcolor='white')
    #fig.show()
    return fig
# dataPath = os.path.abspath(os.path.join(os.path.dirname((os.path.curdir.__dir__()[0])), '..', 'Data'))
# figs = volatility('2222.SE',pd.read_csv(dataPath+'\\2222.SE\\Fundamentals.csv'),pd.read_csv(dataPath+'\\2222.SE\\Peers.csv'))
# figs.show()
test = "Equity-Eagle\AllStockNames.csv"
dataPath = os.path.abspath(os.path.join(os.path.dirname((os.path.curdir.__dir__()[0])), '..', 'Equity-Eagle'))

@st.cache()
def get_stock_names():
    df = pd.read_csv(test)
    company_names = list(df['Company Common Name'])
    return company_names



with st.sidebar:
    st.title('Asset Selection')
    ticker = st.selectbox('Choose an Equity',get_stock_names())
st.title(ticker)

'''
Add in the data gathering code under here:
'''
dataPath = os.path.abspath(os.path.join(os.path.dirname((os.path.curdir.__dir__()[0])), '..', 'Equity-Eagle'))
df = pd.read_csv("C:\\Users\\paulv\\Documents\\Uni\\Hackathon\\Equity-Eagle\\AllStockNames.csv")
name = ticker
ticker = df.loc[df['Company Common Name'] == ticker]['Updated at 18:21:34'][0]


ek.set_app_key('04c0e3f661bd49348d69c3aabedb8c0108cfd1e2')
#start and end date; it is in format yyyy-mm-dd
now = dt.datetime.now()
start = now - dt.timedelta(days = 365*25)

#initialising demo of generating timeseries for list of stock tickers
dfs = list()
myDir = ("Data")
dataPath = os.path.abspath(os.path.join(os.path.dirname((os.path.curdir.__dir__()[0])), '..', 'Data')) #goes up a dir to equity eagle then into Data dir
#get all tickers currently downloaded

#need to check if ticker user inputted in top 5000? design decision tbd
    #check if ticker downloaded
dataPath = "Equity-Eagle\\Data\\{}".format(ticker)
temp = os.path.exists(dataPath)
if os.path.isdir(dataPath):
    #get news df
    df = ek.get_news_headlines('PresetTopic:[Significant News: All] AND R:{} AND Language:LEN'.format(ticker), count=5)
    df['HTML'] = df['storyId'].apply(ek.get_news_story) #create col with article html
    #get sentiments and objectivity
    df['Polarity'] = np.nan
    df['Subjectivity'] = np.nan
    df['Score'] = np.nan

    for idx, storyId in enumerate(df['storyId'].values):
        newsText = ek.get_news_story(storyId) #get the news story
        if newsText:
            soup = BeautifulSoup(newsText,"lxml") #create a BeautifulSoup object from our HTML news article
            sentA = TextBlob(soup.get_text()) #pass the text only article to TextBlob to anaylse
            df['Polarity'].iloc[idx] = sentA.sentiment.polarity #write sentiment polarity back to df
            df['Subjectivity'].iloc[idx] = sentA.sentiment.subjectivity #write sentiment subjectivity score back to df
            if sentA.sentiment.polarity >= 0.05: # attribute bucket to sentiment polartiy
                score = 'positive'
            elif  -.05 < sentA.sentiment.polarity < 0.05:
                score = 'neutral'
            else:
                score = 'negative'
            df['Score'].iloc[idx] = score #write score back to df
    
    #check if news csv exists- superflous????      
    if os.path.exists(dataPath + "\\News.csv"):
        #overwrite csv
        df.to_csv(path_or_buf=dataPath+"\\News.csv",mode='w')

    else:
        #create csv and write top 5
        df.to_csv(path_or_buf=dataPath+"\\News.csv",mode='w')
else:
    #make dir and add 

    #add timeseries csv
    df = ek.get_timeseries(ticker,'CLOSE',interval='daily',start_date=start,end_date=now)
    os.makedirs(dataPath)
    df.to_csv(path_or_buf = dataPath + "\Prices.csv")

    #add peers csv
    df,err = ek.get_data('PEERS("{}")'.format(ticker),
    [
    'TR.F.EVToEBIT','TR.F.EVToEBITDA','TR.EVToSales(1D)','TR.FwdPtoEPSSmartEst','TR.PriceToBVPerShare',
    'TR.PriceToCFPerShare','TR.PriceClose/TR.FreeOperatingCashFlowperShareAvgDilutedSharesOut','TR.Volatility260D/100',
    'TR.ReturnonAvgTotEqtyPctNetIncomeBeforeExtraItems/100', 'TR.ROATotalAssetsPercent/100','TR.GrossMargin/100',
    'TR.NetIncome/TR.Revenue','TR.LTDebtToTtlEqtyPct/100','TR.LTDebtToTtlCapitalPct/100','TR.TimesInterestEarned',
    'PERATIO'
    ])
    df['Price / EPS (SmartEstimate ®)'] = pd.to_numeric(df['Price / EPS (SmartEstimate ®)'],errors='coerce') #remove nan string in starMine col
    df = df.dropna(axis=0,how='any')
    df.to_csv(path_or_buf = dataPath + "\Peers.csv")

    #add fundamentals csv
    df,err = ek.get_data(ticker,
    [
    'TR.F.EVToEBIT','TR.F.EVToEBITDA','TR.EVToSales(1D)','TR.FwdPtoEPSSmartEst','TR.PriceToBVPerShare',
    'TR.PriceToCFPerShare','TR.PriceClose/TR.FreeOperatingCashFlowperShareAvgDilutedSharesOut', 'TR.Volatility260D/100',
    'TR.ReturnonAvgTotEqtyPctNetIncomeBeforeExtraItems/100', 'TR.ROATotalAssetsPercent/100','TR.GrossMargin/100',
    'TR.NetIncome/TR.Revenue','TR.LTDebtToTtlEqtyPct/100','TR.LTDebtToTtlCapitalPct/100','TR.TimesInterestEarned',
    'TR.BusinessSummary','TR.BusinessSummary','TR.OrgFoundedYear','TR.CompanyNumEmploy','TR.OrganizationWebsite',
    'TR.Revenue','TR.CompanyMarketCap','TR.RepNetProfitMean','PERATIO','TR.PriceToSalesPerShare',
    'TR.F.COGSTot','TR.DividendYield','TR.F.DivPayoutRatioPct/100'
    ])
    df['Price / EPS (SmartEstimate ®)'] = pd.to_numeric(df['Price / EPS (SmartEstimate ®)'],errors='coerce') #remove nan string in starMine col
    df = df.dropna(axis=0,how='any')
    df.to_csv(path_or_buf = dataPath + "\Fundamentals.csv")





st.write('---')
st.header(f'{name} Company Overview')
st.subheader('1.1 Description')
description = pd.read_csv(dataPath+'\\Fundamentals.csv')['Business Description'][0]
st.write(description)

#1.2 Stock performance Graph
st.subheader('1.2 Stock Performance')
df = yf.download('KO',dt.date(2000,1,1),dt.date.today(),progress=False)
df['Close'] = df['Close'].round(2)
fig =equity_graph(df)
st.plotly_chart(fig,use_container_width=True)


#1.3 Recent Peer performance 
st.subheader('1.3 Recent Annual Peer performance')
col1, col2, col3, col4, col5 = st.columns(5)
col1.metric("Tesla", "$213.32", "2.5%")
col2.metric("Bitcoin", "$20,345", "-5.2%")
col3.metric("Coca Cola", "$23.32", "2.3%")
col4.metric("General Dynamics", "$245.32", "-5.3%")
col5.metric("Lockheed Martin", "$13.32", "9.2%")
col1.metric("Tesla", "$213.32", "2.5%")
col2.metric("Bitcoin", "$20,345", "-5.2%")
col3.metric("Coca Cola", "$23.32", "2.3%")
col4.metric("General Dynamics", "$245.32", "-5.3%")
col5.metric("Lockheed Martin", "$13.32", "9.2%")


#1.4 Key Metrics Graph
st.subheader('1.4 Key Metrics')
market_cap = 2611000000000
revenue = 387540000000
earnings = 95170000000
pe_ratio = 12.5 
ps_ratio = 4.5
fig = bar_fig(market_cap,revenue,earnings,pe_ratio,ps_ratio)
st.plotly_chart(fig,use_container_width=True)

#1.5 Income Statement Brief
st.subheader('1.5 Income Statement Brief')
revenue = 100000000000
cost_of_sales = 20000000000
gross_profit = 80000000000
other_expenses = 20000000000
net_income = 60000000000
fig = income_statement_bar(revenue,cost_of_sales,gross_profit,other_expenses,net_income)
st.plotly_chart(fig,use_container_width=True)

#1.6 Peer PE Comparison
st.subheader('1.6 Peer PE Comparison')
fig = peer_PE_bar()
st.plotly_chart(fig,use_container_width=True)


st.subheader('1.7 Peer Volatility Comparison')
fig = volatility('AAPL.OQ')
st.plotly_chart(fig,use_container_width=True)


st.subheader('1.8 NLTK Ajusted News')
col1, col2, col3 = st.columns([1,2,5])












