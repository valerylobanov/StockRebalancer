import math
import pandas as pd
pd.options.mode.chained_assignment = None  # default='warn'
import numpy as np
from IPython.display import display
import Moex as mx

'''
tgt - target
chg - change (delta)
'''
class Portfolio:

    tolerance = 0
    
    def __init__(self,tolerance=0):
        pd.options.display.float_format = '{:,.2f}'.format
        self.tolerance = tolerance
    
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
        moex = mx.Moex()
        # moex.quotes.to_csv('moex_quotes.csv')
        self.current = self.current.join(moex.quotes,how='outer')
        self.current.fillna(value=0,inplace=True)
        #self.current.to_csv('self_current.csv')
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

    def rebalance(self):

        df = self.target.join(self.current,lsuffix='Tgt')

        totalPortfolio = self.__getTotal()
        x = self.findNonZeroLots(df,totalPortfolio)

        # target value
        x['valueTgt'] = x['percentTgt'] * totalPortfolio
        x['lotQtyTgt'] = (x['valueTgt'] / x['price']/x['lotSize']).apply(np.floor) 
        x['qtyTgt'] = x['lotQtyTgt'] * x['lotSize']
        
        # change = to be - as is
        x['chgQty'] = x['qtyTgt'] - x['qty']
        x['chgValue'] = x['chgQty']*x['price']

        x = x.drop(x[x.chgValue <= 0].index)

        # drop smallest value until sum is positive
        # while x['chgValue'].sum() > 0:
        #     x = x.drop(x[x.chgValue == x['chgValue'].min() ].index)

        # display(x [x.chgValue == x['chgValue'].min()].index )

        while x['chgValue'].sum() > self.cash:
            x = x.drop(x [x.chgValue == x['chgValue'].min()].index ) 
  

        # only columns and rows needed for future processing
        r = pd.DataFrame(x[['chgQty','chgValue']].dropna())

        # display(r)
        
        return r.sort_values(by=['chgValue'],ascending=False)

    # can buy whole lot and it's value is above tolerance
    def findNonZeroLots(self,x,totalPortfolio):
        x['valueTgt'] = x['percentTgt'] * totalPortfolio
        x['lotQtyTgt'] = (x['valueTgt'] / x['price']/x['lotSize']).apply(np.floor) 
        # x.to_csv('x.csv')
        return x.loc[ (x['lotQtyTgt']>0) & (x['valueTgt'] > self.tolerance) ]

    def applyChanges(self,dfChanges):
        """
        dfChages - DataFrame
        - ticker - string, index
        - chgQty - int, difference to apply
        - chgValue - float, difference to apply
        """
       
        # set new stocks
        self.current = Portfolio.__sumChanges(self.current,dfChanges)

        # set cash in reverse to stocks
        self.cash = self.cash - dfChanges['chgValue'].sum()

        self.current['percent'] = self.current['price']*self.current['qty'] / self.__getTotal()
        self.current = self.current.sort_values(by=['percent'],ascending=False)

    @staticmethod
    def __sumChanges(dfCurrent, dfChanges):
        
        x = dfCurrent.join(dfChanges,how='left')
        x = x.fillna(0)
        display(x)
        x['qty'] = x['qty'] + x['chgQty']
        x['value'] = x['value'] + x['chgValue']

        return x


    def getStd(self,verbouse = False):
        """ std deviation as rebalance quality criteria """
        df = self.target.join(self.current,lsuffix='Tgt')
        ttl = self.__getTotal()
        df['valueTgt'] = df['percentTgt']*ttl
        df['value'] = df['value'].fillna(0)
        df['delta'] = df['value'] - df['valueTgt']

        std = np.std(df['delta'])
        if verbouse:
            dd = df[['value','valueTgt','delta']]
            dd['delta %'] = dd['delta'] / self.__getTotal() * 100
            dd['value'] = dd['value'] / 1000
            dd['valueTgt'] = dd['valueTgt']/1000
            dd['delta'] = dd['delta']/1000
            display(dd)

            display(dd[dd['delta %']==dd['delta %'].max()])
            display(dd[dd['delta %']==dd['delta %'].min()])
            print(f'std  = {std:,.0f}')

        return std