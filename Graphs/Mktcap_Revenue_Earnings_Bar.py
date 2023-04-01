import pandas as pd 
import plotly.graph_objects as go 
import yfinance as yf
from numerize import numerize



#Graph: Market cap, Revenue, Earnings, PE, PS
market_cap = 2611000000000
revenue = 387540000000
earnings = 95170000000

def mktcap_revenue_earnings_bar(market_cap,revenue,earnings):
	fig = go.Figure(go.Bar(
	            x=[earnings,revenue,market_cap],
	            y=['Earnings','Revenue','Market Cap'],
	            orientation='h',
	            marker_color = ['green','blue','navy'],
	            width = [1,1,1],
	            text = [
	            	f'Earnings {numerize.numerize(earnings)}',
	            	f'Revenue {numerize.numerize(revenue)}',
	            	f'Market Cap {numerize.numerize(market_cap)}'
	            	]
	            ))
	fig.update_traces(
		textfont_size=12,
		textangle=0,
		textposition="outside",
		cliponaxis=False
		)
	fig.update_layout(
		plot_bgcolor="white",
		bargap=0
		)
	fig.update_xaxes(
		showticklabels=False
		)
	fig.update_layout(
		height=400,
		width=1000
		)
	fig.update_yaxes(
		showticklabels=False
		)
	fig.show()


mktcap_revenue_earnings_bar(market_cap,revenue,earnings)



