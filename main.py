import pandas as pd
import numpy as np
from IPython.display import display

import Portfolio as pf
import Imoex as im

#  what we have
currentQty = pd.read_csv('current.csv',\
                dtype={'ticker': np.str_, 'qty': np.int_},\
                index_col='ticker'
                    )
cash = 227000

# what we want
imoex = im.Imoex()
tgtPercentage = imoex.getIndex()

# setup portfolio
p = pf.Portfolio()
p.setTarget(tgtPercentage)
p.setCurrent(currentQty,cash)
c1 = p.getCashValue()
a1 = p.getStocksValue()

# rebalance
c = p.rebalance(10000)
p.applyChanges(c)
c2 = p.getCashValue()
a2 = p.getStocksValue()

# output results
print(f'before cash {c1:,.0f} stocks {a1:,.0f} total {(a1+c1):,.0f}')
print(f'after cash {c2:,.0f} stocks {a2:,.0f} total {(a2+c2):,.0f}')
display(c)
print(len(c.index))