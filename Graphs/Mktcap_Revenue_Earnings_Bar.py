import pandas as pd 
import plotly.graph_objects as go 
import yfinance as yf
from numerize import numerize
from plotly.subplots import make_subplots




#Graph: Market cap, Revenue, Earnings, PE, PS
market_cap = 2611000000000
revenue = 387540000000
earnings = 95170000000
pe_ratio = 12.5 
ps_ratio = 4.5

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
		width=1200
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
		y=80,
	    text=f'{pe_ratio}x',
	    font=dict(size=30,color='navy'),
	    showarrow=False,
	    arrowhead=1,
	    row=1,
	    col=2
	    )
	fig.add_annotation(
		x=75,
		y=80,
	    text=f'{ps_ratio}x',
	    font=dict(size=30,color='navy'),
	    showarrow=False,
	    arrowhead=1,
	    row=1,
	    col=2
	    )
	fig.add_annotation(
		x=25,
		y=65,
	    text='PE Ratio',
	    font=dict(size=18,color='navy'),
	    showarrow=False,
	    arrowhead=1,
	    row=1,
	    col=2
	    )
	fig.add_annotation(
		x=75,
		y=65,
	    text='PS Ratio',
	    font=dict(size=18,color='navy'),
	    showarrow=False,
	    arrowhead=1,
	    row=1,
	    col=2
	    )
	fig.show()


bar_fig(market_cap,revenue,earnings,pe_ratio,ps_ratio)




