import time
import pandas as pd
from IPython.display import display
import requests
import bs4
import os

class Imoex:

    index = pd.DataFrame(columns=[ 'percent', 'price', 'name'],index=['ticker'])

    def __init__(self):

        timestr = time.strftime("%Y%m%d")
        fname = f'ImoexData/Imoex{timestr}.csv'

        self.fetchToFile(fname)

        self.index = pd.read_csv(fname,index_col='ticker')

    def getIndex(self):
        return self.index

    def fetchToFile(self, fname):
        if not(os.path.exists(fname)):
            url = 'https://smart-lab.ru/q/index_stocks/IMOEX/#'
            response = requests.get(url)

            soup = bs4.BeautifulSoup(response.text, 'html.parser')
            table = soup.find_all('table')[0]
            rows = table.find_all('tr')

            index = pd.DataFrame(columns=[ 'percent', 'price', 'name'],index=['ticker'])

            for row in rows[1:]:
                cells = row.find_all('td')

                name = cells[1].text.strip()

                percent = float(cells[2].text.strip().strip('%'))

                ticker_href = cells[3].find_all('a')[0].get('href')
                ticker = ticker_href[9:]

                price = cells[5].text.strip()

                index.loc[ticker] = [percent,price,name]

            index = index.dropna()

            excluded = pd.read_csv('exclude.csv',index_col=0)
            index = index.drop(excluded.index,errors='ignore')

            index.to_csv(fname,index_label='ticker')

        # display(df)