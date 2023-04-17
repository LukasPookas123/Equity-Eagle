import eikon as ek
import pandas as pd
import datetime as dt
import os
from bs4 import BeautifulSoup
from textblob import TextBlob
import numpy as np


class csvConstructor():

    def testRun(self):
        RICs = ['AAPL.OQ','MSFT.OQ',"2222.SE",'GOOGL.OQ','AMZN.OQ']
        for ticker in RICs:
            self.readTicker(ticker)

    def readTicker(self, ticker):
        #set app key to identify the application on Refinitiv Platform
        ek.set_app_key('04c0e3f661bd49348d69c3aabedb8c0108cfd1e2')

        #start and end date; it is in format yyyy-mm-dd
        now = dt.datetime.now()
        start = now - dt.timedelta(days = 365*25)

        #initialising demo of generating timeseries for list of stock tickers
        dataPath = os.path.abspath(os.path.join(os.getcwd(),'Data')) #goes up a dir to equity eagle then into Data dir
        #get all tickers currently downloaded

        #need to check if ticker user inputted in top 5000? design decision tbd
        #check if ticker downloaded
        dataPath = "Equity-Eagle\\Data\\{}".format(ticker)
        if os.path.isdir(dataPath):
            #ADD IN PRICE UPDATE EACH SEARCH
            df = ek.get_timeseries(ticker,'CLOSE',interval='daily',start_date=start,end_date=now)
            df.to_csv(path_or_buf = dataPath + "\Prices.csv")

        else:
            #make dir and add 

            #add timeseries csv
            df = ek.get_timeseries(ticker,'CLOSE',interval='daily',start_date=start,end_date=now)
            os.makedirs(dataPath)
            df.to_csv(path_or_buf = dataPath + "\Prices.csv")

            #add fundamentals csv
            df,err = ek.get_data(ticker,
            [
            'TR.GrossMargin/100','TR.F.OthNonOpIncExpnTot(Period=FY0)','TR.Revenue','TR.CompanyMarketCap',
            'TR.RepNetProfitMean','PERATIO','TR.PriceToSalesPerShare', 'TR.NetIncome', 'TR.GrossIncomeMean(Period=FY1)',
            'TR.ClosePrice.Date','TR.ClosePrice','TR.F.COGSInclOpMaintUtilTot(Period=FY0)',
            ])
            df = df.dropna(axis=0,how='any')
            df.to_csv(path_or_buf = dataPath + "\Fundamentals.csv")
        
dc = csvConstructor()
dc.testRun()

'''
    need to rename columns
    fundamental data:
    -company overview: description, founded, employees, ceo, website
    =stock graph
    =volatility vs peers average
    -revenue
    -market cap
    -earnings
    -PE
    -PS
    -All peers metrics
    -Cost of revenue
    -current dividen yield
    -payout ratio
'''