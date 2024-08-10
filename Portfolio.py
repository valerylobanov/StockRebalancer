import math
import pandas as pd
pd.options.mode.chained_assignment = None  # default='warn'
import numpy as np
from IPython.display import display
import StockData as sd

# TODO load quotes from moex

'''
tgt - target
chg - change (delta)
'''
class Portfolio:
    
    def __init__(self,dfTarget):
        self.assets = dfTarget.rename(columns={"percent": "tgtPercent"})
        self.assets['tgtPercent'] = self.assets['tgtPercent']/100
    
    # dfCurrent = {ticker: string,index; quantity: int}
    def setCurrent(self,dfCurrent,cash):
        self.assets = self.assets.join(dfCurrent)
        self.cash = cash

        # get current quotes
        moex = sd.Moex()
        self.assets = self.assets.join(moex.quotes)
        print('hello')
        
        # TODO: apply stocks.getPrice, getLotSize

        # self.assets['lot_qty'] = 0
        # self.assets['lot_qty'] = self.assets['lot_qty'].apply(lambda x: x+1)
        # display(self.assets)
        
        self.assets['percent'] = self.assets['price']*self.assets['qty'] / self.__getTotal()
           
    def __getTotal(self):
        return (self.assets['qty']*self.assets['price']).sum() + self.cash 

    def __getError(self):
        return np.square(np.subtract(self.assets['tgtPercent'],self.assets['percent'])).mean()*100   

    def display(self):     

        # a = self.assets[self.assets.qty>0]
        a = self.assets

        a['value'] = a['qty']*a['price']

        b = self.getStats(a) 
        df = pd.concat([a,b])

        self.formatColumns(df)

        display(df)
        print('sqrt error = {0:.2f}'.format(self.__getError())) 

    def getStats(self, a):
        b = pd.DataFrame(columns=['tgtPercent','qty','price','lot_qty','percent','value','chgValue'],\
                        index=['stock ttl','cash','total'])
        
        b['tgtPercent']['stock ttl'] = a['tgtPercent'].sum()
        
        b['value']['stock ttl'] = a['value'].sum()
        b['value']['cash'] = self.cash
        b['value']['total'] = b['value']['stock ttl']+b['value']['cash']
        
        b['percent']['stock ttl'] =  b['value']['stock ttl'] / b['value']['total']
        b['percent']['cash'] =  1 - b['percent']['stock ttl']
        b['percent']['total'] =  1
        return b

    def formatColumns(self, df):
        df['percent'] = df['percent'].map('{:.1%}'.format)
        df['tgtPercent'] = df['tgtPercent'].map('{:.1%}'.format)
        df['qty'] = df['qty'].map('{:.0f}'.format)
        df['lot_qty'] = df['lot_qty'].map('{:.0f}'.format)
        df['price'] = df['price'].map('{:,.0f}'.format)
        df['value'] = df['value'].map('{:,.0f}'.format)

    def rebalance2(self):
        totalPortfolio = self.__getTotal()
        x = Portfolio.findNonZeroLots(self.assets,totalPortfolio)

        # make sum(percent) = 100%
        x['tgtPercent'] = x['tgtPercent'] / x['tgtPercent'].sum()

        # target value
        x['tgtValue'] = x['tgtPercent'] * totalPortfolio
        x['tgtLotQty'] = (x['tgtValue'] / x['price']/x['lot_qty']).apply(np.floor) 
        x['target_qty'] = x['tgtLotQty'] * x['lot_qty']
        
        # change = to be - as is
        x['chgQty'] = x['target_qty'] - x['qty']
        x['chgValue'] = x['chgQty']*x['price']

        # only columns and rows needed for future processing
        r = pd.DataFrame(x[['chgQty','chgValue']].dropna())
        # r['chgValue'] = r['chgValue'].map('{:,.0f}'.format)
        # r['chgQty'] = r['chgQty'].map('{:,.0f}'.format)
        
        return r.sort_values(by=['chgValue'],ascending=False)

    # can buy whole lot and it's value is above tolerance
    @staticmethod
    def findNonZeroLots(x,totalPortfolio, tolerance=20000):
        x['tgtValue'] = x['tgtPercent'] * totalPortfolio
        x['tgtLotQty'] = (x['tgtValue'] / x['price']/x['lot_qty']).apply(np.floor) 
        return x.loc[ (x['tgtLotQty']>0) & (x['tgtValue'] > tolerance) ]