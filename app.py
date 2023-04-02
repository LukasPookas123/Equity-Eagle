import pandas as pd
import streamlit as st
import yfinance
from streamlit_card import card
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
#from numerize import numerize

@st.cache_data
def load_data():
    components = pd.read_html('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')[0]
    return components.set_index('Symbol')

@st.cache_data
def load_quotes(asset):
    return yfinance.download(asset)


def main():
    components = load_data()
    title = st.empty()
    st.sidebar.title("Options")

    def label(symbol):
        a = components.loc[symbol]
        return symbol + ' - ' + a.Security

    st.sidebar.subheader('Select asset')
    asset = st.sidebar.selectbox('Click below to select a new asset',
                                 components.index.sort_values(), index=3,
                                 format_func=label)
    title.title(components.loc[asset].Security)
    
    if st.sidebar.checkbox('View company info', True):
        st.table(components.loc[asset])
    data0 = load_quotes(asset)
    data = data0.copy().dropna()
    data.index.name = None

    # PRINTING STOCK DATA
    # print(data)

    section = st.sidebar.slider('Number of quotes', min_value=30,
                        max_value=min([2000, data.shape[0]]),
                        value=500,  step=10)

    # DISPLAYING HISTORICAL DATA -> Adj Close - [-section:] takes number of data points requested
    data2 = data[-section:]['Adj Close'].to_frame('Adj Close')

    sma = st.sidebar.checkbox('SMA')
    if sma:
        period= st.sidebar.slider('SMA period', min_value=5, max_value=500,
                             value=20,  step=1)
        data[f'SMA {period}'] = data['Adj Close'].rolling(period ).mean()
        data2[f'SMA {period}'] = data[f'SMA {period}'].reindex(data2.index)

    sma2 = st.sidebar.checkbox('SMA2')
    if sma2:
        period2= st.sidebar.slider('SMA2 period', min_value=5, max_value=500,
                             value=100,  step=1)
        data[f'SMA2 {period2}'] = data['Adj Close'].rolling(period2).mean()
        data2[f'SMA2 {period2}'] = data[f'SMA2 {period2}'].reindex(data2.index)

    st.subheader('Chart')
    st.line_chart(data2)

    if st.sidebar.checkbox('View stadistic'):
        st.subheader('Stadistic')
        st.table(data2.describe())

    if st.sidebar.checkbox('View quotes'):
        st.subheader(f'{asset} historical data')
        st.write(data2)

    with open('cardstyle.css') as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)

    col1.metric("Temperature", "70 °F", "1.2 °F")
    col2.metric("Wind", "9 mph", "-8%")
    col3.metric("Humidity", "86%", "4%")

    # HORIZONTAL BAR CHART

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

    st.plotly_chart(fig)

if __name__ == '__main__':
    main()
