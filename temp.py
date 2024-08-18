import pandas as pd
import numpy as np
from IPython.display import display
import Portfolio as pf



'''
test data
''' 

#  what we have
currentQty = pd.read_csv('current.csv',\
                dtype={'ticker': np.str_, 'qty': np.int_},\
                index_col='ticker'
                    )
cash = 600000

#  what we want
tgtPercentage = pd.read_csv('moex.csv',\
                dtype={'ticker': np.str_, 'percent': np.float64},\
                index_col='ticker'
                    )

'''
setup
'''

p = pf.Portfolio()
p.setTarget(tgtPercentage)
p.setCurrent(currentQty,10000000)

s1 = p.getStd()
c1 = p.getCashValue()
a1 = p.getStocksValue()

'''
assertions
'''

c = p.rebalance2()
p.applyChanges(c)

s2 = p.getStd()
c2 = p.getCashValue()
a2 = p.getStocksValue()

# assert s2 < s1
# assert c2 < c1
# assert a2 > a1


print(f'before cash {c1:,.0f} stocks {a1:,.0f} total {(a1+c1):,.0f}')
print(f'after cash {c2:,.0f} stocks {a2:,.0f} total {(a2+c2):,.0f}')