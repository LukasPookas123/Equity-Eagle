import plotly.graph_objects as go
import streamlit as st
from numerize import numerize

revenue = 100000000000
cost_of_sales = 20000000000
gross_profit = 80000000000
other_expenses = 20000000000
net_income = 60000000000

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
	fig.show()


income_statement_bar(revenue,cost_of_sales,gross_profit,other_expenses,net_income)

