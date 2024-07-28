import math
import pandas as pd
pd.options.mode.chained_assignment = None  # default='warn'
import numpy as np
from IPython.display import display


class Portfolio:
    
    def __init__(self,dfTarget):
        self.assets = dfTarget.rename(columns={"percent": "target_percent"})
        self.assets['target_percent'] = self.assets['target_percent']/100
    # dfCurrent = {ticker: string,index; quantity: int, price: float}
    def setCurrent(self,dfCurrent,cash):

        self.assets = self.assets.join(dfCurrent)
        self.cash = cash
        self.assets['percent'] = self.assets['price']*self.assets['qty'] / self.__getTotal()
           
    def __getTotal(self):
        return (self.assets['qty']*self.assets['price']).sum() + self.cash 

    def __getError(self):
        return np.square(np.subtract(self.assets['target_percent'],self.assets['percent'])).mean()*100   

    def display(self):     

        a = self.assets[self.assets.qty>0]
        a['value'] = a['qty']*a['price']

        n = np.nan
        b = pd.DataFrame([[a['target_percent'].sum(),n,n,n,a['percent'].sum(),a['value'].sum(),n],\
                          [0,n,n,n,self.cash/self.__getTotal(),self.cash,n],\
                            [n,n,n,n,1,self.__getTotal(),n]],\
                              columns=['target_percent','qty','price','lot_qty','percent','value','change_value'],\
                                index=['[stock ttl]','[cash]','[total]'])
        
        df = pd.concat([a,b])

        self.formatColumns(df)
        display(df)

        print('sqrt error = {0:.2f}'.format(self.__getError())) 

    def formatColumns(self, df):
        df['percent'] = df['percent'].map('{:.1%}'.format)
        df['target_percent'] = df['target_percent'].map('{:.1%}'.format)
        df['qty'] = df['qty'].map('{:.0f}'.format)
        df['lot_qty'] = df['lot_qty'].map('{:.0f}'.format)
        df['price'] = df['price'].map('{:,.0f}'.format)
        df['value'] = df['value'].map('{:,.0f}'.format)

    def rebalance2(self):
        totalPortfolio = self.__getTotal()
        x = Portfolio.findNonZeroLots(self.assets,totalPortfolio)

        # make sum(percent) = 100%
        x['target_percent'] = x['target_percent'] / x['target_percent'].sum()

        # target value
        x['target_value'] = x['target_percent'] * totalPortfolio
        x['target_lot_qty'] = (x['target_value'] / x['price']/x['lot_qty']).apply(np.floor) 
        x['target_qty'] = x['target_lot_qty'] * x['lot_qty']
        
        # change = to be - as is
        x['change_qty'] = x['target_qty'] - x['qty']
        x['change_value'] = x['change_qty']*x['price']

        # only columns and rows needed for future processing
        r = pd.DataFrame(x[['change_qty','change_value']].dropna())
        r['change_value'] = r['change_value'].map('{:,.0f}'.format)
        r['change_qty'] = r['change_qty'].map('{:,.0f}'.format)
        
        return r

    @staticmethod
    def findNonZeroLots(x,totalPortfolio):
        x['target_value'] = x['target_percent'] * totalPortfolio
        x['target_lot_qty'] = (x['target_value'] / x['price']/x['lot_qty']).apply(np.floor) 
        return x.loc[x['target_lot_qty']>0]