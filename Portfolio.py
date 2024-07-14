import math
import pandas as pd
import numpy as np
from IPython.display import display


class Portfolio:
    
    # def __init__(self,assets,cash):

        # self.assets = assets
        # self.assets.set_index("ticker")
        
        # self.cash = cash
        

        # self.total = (self.assets['quantity']*self.assets['price']).sum() + self.cash  

        # self.__recalcColumns()

    # dfTarget = {ticker:string, index; percent:float (0-100)}
    def __init__(self,dfTarget):
        self.assets = dfTarget.rename(columns={"percent": "target_percent"})

    # dfCurrent = {ticker: string,index; quantity: int, price: float}
    def setCurrent(self,dfCurrent,cash):
        self.assets = self.assets.join(dfCurrent)
        self.cash = cash
        self.assets['percent'] = self.assets['price']*self.assets['quantity'] / self.__getTotal()
           
    def __getTotal(self):
        return (self.assets['quantity']*self.assets['price']).sum() + self.cash 

    def __getError(self):
        return np.square(np.subtract(self.assets['target_percent'],self.assets['percent'])).mean()*100
        # return 0

    # def setTarget(self,target):

    #     target.set_index("t_ticker") # TODO: rename during join

    #     self.assets = self.assets.join(target)
        
    #     # make sum of % = 100%
    #     self.assets['target %'] = self.assets['target %']/ self.assets['target %'].sum()

        

    def display(self):     
        display(self.assets)
        print('cash = {0:.2f}'.format(self.cash))
        print('sqrt error = {0:.2f}\n\n'.format(self.__getError())) 
        print('total = {0:.2f}\n\n'.format(self.__getTotal()))
        
    # def __recalcColumns(self):

    #     # self.assets['%'] = self.assets['price']*self.assets['quantity'] / self.total
  
    #     # assetsTotal = (self.assets['quantity']*self.assets['price']).sum()
    #     # self.cash = self.total - assetsTotal

    #     self.total = (self.assets['quantity']*self.assets['price']).sum() + self.cash  

        # TODO: add "if exists"
        #self.error = np.square(np.subtract(self.assets['target %'],self.assets['%'])).mean()*100
  
    def rebalance(self):
        # print('hello')

        # estimated quatity - 1st pass with rounding
        self.assets['target_value'] = self.assets['target_percent'] * self.__getTotal()
        
        self.assets['temp_quantity'] = (self.assets['target_value'] / self.assets['price']).round()
        self.assets['temp_value'] = self.assets['temp_quantity']*self.assets['price']
        self.assets['temp_delta'] = self.assets['target_value'] - self.assets['temp_value']
        temp_total = self.assets['temp_value'].sum()

    #     # use cash remainder for additional assets. We're using asset with lowest price for this (simplest method)
    #     minPrice = self.assets['price'].min()
    #     addQty = math.floor(self.cash/minPrice)
    #     self.assets.loc[ self.assets['price'] == minPrice, 'quantity' ] = self.assets['quantity'] + addQty

    #     self.__recalcColumns()