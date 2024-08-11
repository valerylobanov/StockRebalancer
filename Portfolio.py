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
    
    def __init__(self):
        pd.options.display.float_format = '{:,.2f}'.format

    def setTarget(self,percentages):
        """
        set target percentage of stocks in Portfolio\n
        - percentages -  DataFrame {ticker: string,index; percent: 0..1 float}
        """
        self.target = percentages
        totalPct = self.target['percent'].sum()
        self.target['percent'] = self.target['percent']/totalPct
    
    def getTarget(self):
        return self.target
    
    def setCurrent(self,quantities,cash):
        """
        set current qty of stocks in Portfolio\n
        - quantities {ticker: string,index; qty: int} - quantities\n
        - cash
        """
        self.current = quantities
        self.cash = cash

        # get current quotes
        moex = sd.Moex()
        self.current = self.current.join(moex.quotes)
        self.current['percent'] = self.current['price']*self.current['qty'] / self.__getTotal()

        self.current['value']=self.current['price']*self.current['qty']
    
    def getCurrent(self):
        return self.current

    def getStocksValue(self):     
        return self.current['value'].sum()
    
    def getCashValue(self):
        return self.cash
           
    def __getTotal(self):
        return (self.current['qty']*self.current['price']).sum() + self.cash 

    def getRebalanceChanges(self):

        df = self.target.join(self.current,lsuffix='Tgt')

        totalPortfolio = self.__getTotal()
        x = Portfolio.findNonZeroLots(df,totalPortfolio)


        # target value
        x['valueTgt'] = x['percentTgt'] * totalPortfolio
        x['lotQtyTgt'] = (x['valueTgt'] / x['price']/x['lotSize']).apply(np.round) 
        x['qtyTgt'] = x['lotQtyTgt'] * x['lotSize']
        
        # change = to be - as is
        x['chgQty'] = x['qtyTgt'] - x['qty']
        x['chgValue'] = x['chgQty']*x['price']

        # only columns and rows needed for future processing
        r = pd.DataFrame(x[['chgQty','chgValue']].dropna())
        
        return r.sort_values(by=['chgValue'],ascending=False)

    # can buy whole lot and it's value is above tolerance
    @staticmethod
    def findNonZeroLots(x,totalPortfolio, tolerance=0):
        x['valueTgt'] = x['percentTgt'] * totalPortfolio
        x['lotQtyTgt'] = (x['valueTgt'] / x['price']/x['lotSize']).apply(np.floor) 
        return x.loc[ (x['lotQtyTgt']>0) & (x['valueTgt'] > tolerance) ]

    def rebalance(self):
        c = self.getRebalanceChanges()
        self.current = self.current.join(c)
        
        # saving for debug
        self.current['qtyPrev'] = self.current['qty']
        self.current['valuePrev']  = self.current['value']

        # set new stocks
        self.current['qty'] = self.current['qtyPrev'] + self.current['chgQty']
        self.current['value'] = self.current['valuePrev'] + self.current['chgValue']

        # set cash in reverse to stocks
        self.cash = self.cash - self.current['chgValue'].sum()

        # drop change collumns to enable future rebalances
        self.current = self.current.drop('chgQty',axis=1)
        self.current = self.current.drop('chgValue',axis=1)
