import pandas as pd
import numpy as np
from IPython.display import display

""""
    test data
"""

# setup what we have
currentQty = pd.read_csv('current.csv',\
                 dtype={'ticker': np.str_, 'qty': np.int_},\
                  index_col='ticker'
                    )
print('\ncurrentQty')
display(currentQty)

cash = 600000
print(f"cash {cash:,.0f}\n")

# setup what we want
tgtPercentage = pd.read_csv('moex.csv',\
                 dtype={'ticker': np.str_, 'percent': np.float64},\
                 index_col='ticker'
                    )
print('tgtPercentage head()')
display(tgtPercentage.head())

"""
    setup
"""

import Portfolio as pf

p = pf.Portfolio()
p.setTarget(tgtPercentage)
p.setCurrent(currentQty,600000)


"""
    assertions
"""


# 1st try

s1 = p.getStd()
print('\nrebalance 1')
p.rebalance()
s2 = p.getStd()

print(f"\nstd before {s1:,.0f}")
print(f"std after {s2:,.0f}")
print(f"delta = {(s1-s2)/s1:,.2f}")
print(f"cash  {p.getCashValue():,.0f}")

# 2nd try

s1 = p.getStd()
print('\nrebalance 2')
p.rebalance()
s2 = p.getStd()

print(f"\nstd before {s1:,.0f}")
print(f"std after {s2:,.0f}")
print(f"delta = {(s1-s2)/s1:,.2f}")
print(f"cash  {p.getCashValue():,.0f}")



