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
    
    def setCurrent(self,path):
        
        df = pd.read_csv(path,index_col='ticker')
        df['qty']=df.sum(axis=1)
        self.current=df[['qty']]

        self.cash = self.current.loc['@RUB','qty']
        self.current.drop('@RUB')

        # get current quotes
        moex = mx.Moex()
        self.current = self.current.join(moex.quotes,how='outer')
        self.current.fillna(value=0,inplace=True)
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

        # combine all data together
        df = self.target.join(self.current,lsuffix='Tgt')

        totalPortfolio = self.__getTotal()
        x = self.findNonZeroLots(df,totalPortfolio)

        x['percentTgt'] = x['percentTgt'] / x['percentTgt'].sum()

        # target value
        x['valueTgt'] = x['percentTgt'] * self.cash
        print('sum valueTgt')
        print(x['valueTgt'].sum())

        x['lotQtyTgt'] = x['valueTgt'] / (x['price'] * x['lotSize']) 
        #.apply(np.floor) 
        x['qtyTgt'] = x['lotQtyTgt'] * x['lotSize']

        print('sum valueTgt2')
        x['valueTgt2'] = x['qtyTgt']*x['price']
        print(x['valueTgt2'].sum())
        
        # change = to be - as is

        x['chgQty'] = x['qtyTgt'] - x['qty'] 
        x['chgValue'] = x['chgQty']*x['price']

        print('sum chg val')
        print(x['chgValue'].sum())

        # x = x.drop(x[x.chgValue <= 0].index)

        # while x['chgValue'].sum() > self.cash:
        #     x = x.drop(x [x.chgValue == x['chgValue'].min()].index ) 
  
        # only columns and rows needed for future processing
        # display(x)
        r = pd.DataFrame(x[['nameTgt','chgQty','chgValue']].dropna())
        # r = pd.DataFrame(x[['nameTgt','chgQty','qty','qtyTgt','chgValue']].dropna())
        return r.sort_values(by=['chgValue'],ascending=False)

    # can buy whole lot and it's value is above tolerance
    def findNonZeroLots(self,x,totalPortfolio):

        x['valueTgt'] = x['percentTgt'] * totalPortfolio
        x['lotQtyTgt'] = (x['valueTgt'] / (x['price']*x['lotSize']) ).apply(np.floor) 
        return x.loc[ (x['lotQtyTgt']>0) & ( (x['valueTgt'] -x['value'])> self.tolerance) ]

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
        # display(x)
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