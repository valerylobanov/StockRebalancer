import pandas as pd
import Portfolio as pf
from IPython.display import display
import numpy as np

df = pd.read_csv('moex.csv',\
                 dtype={'ticker': np.str_, 'percent': np.float64},\
                 index_col='ticker'
                    )

dfc = pd.read_csv('current.csv',\
                 dtype={'ticker': np.str_, 'qty': np.int_, 'price': np.float64, 'lot_qty':np.int_},\
                 index_col='ticker'
                    )

p = pf.Portfolio(df)
p.setCurrent(dfc,600000)
p.display()

r2 = p.rebalance2()
display(r2)
print(r2['chgValue'].sum())
