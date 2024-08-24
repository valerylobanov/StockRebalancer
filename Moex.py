import requests
import os
import time
import pandas as pd
from IPython.display import display


class Moex:

    # ticker, lot_aty, price, date, name
    quotes = pd.DataFrame()

    def __init__(self):
        # need to update only onece a day
        timestr = time.strftime("%Y%m%d")
        fname = f'StockData/StockData{timestr}.csv'
        self.__fetchMoexToFile(fname)
        self.quotes = pd.read_csv(fname)
        self.quotes = self.quotes.rename(columns={\
            'SECID':'ticker',\
            'LOTSIZE':'lotSize',\
            'PREVPRICE':'price',\
            'PREVDATE':'date',\
            'LATNAME':'name'})
        self.quotes= self.quotes.set_index('ticker')
        self.quotes = self.quotes.drop(columns=['BOARDID','SHORTNAME','FACEVALUE','STATUS','BOARDNAME',\
                                                'DECIMALS','SECNAME','REMARKS','MARKETCODE','INSTRID','SECTORID',\
                                                'MINSTEP','PREVWAPRICE','FACEUNIT','ISSUESIZE','ISIN',\
                                                'REGNUMBER','PREVLEGALCLOSEPRICE','CURRENCYID','SECTYPE','LISTLEVEL','SETTLEDATE'])

    # get stocks quotes T-1 using MOEX API
    def __fetchMoexToFile(self, fname):
        if not(os.path.exists(fname)):
            url = 'https://iss.moex.com/iss/engines/stock/markets/shares/securities.xml?index=IMOEX&marketprice_board=1'
            response = requests.get(url)
            df = pd.read_xml(response.text,xpath='//data[@id="securities"]/rows/row').set_index('SECID')
            df.to_csv(fname)