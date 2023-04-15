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
        dataPath = "Data\\{}".format(ticker)
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
            
            df.to_csv(path_or_buf=dataPath+"\\News.csv",mode='w')

            #ADD IN PRICE UPDATE EACH SEARCH

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
            
            df.to_csv(path_or_buf=dataPath+"\\News.csv",mode='w')

        
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