import pandas as pd 
import plotly.graph_objects as go 
import streamlit as st
import yfinance as yf
import datetime as dt

#Get Data
df = yf.download('KO',dt.date(2000,1,1),dt.date.today(),progress=False)
df['Close'] = df['Close'].round(2)

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
	fig.show()

equity_graph(df)







