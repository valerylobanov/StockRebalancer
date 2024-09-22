# import pandas as pd
# import numpy as np
# from IPython.display import display
# import Portfolio as pf


# # def test_apply():
   
# #     #  what we have
# #     currentQty = pd.DataFrame( {"qty": [50, 40, 45],'ticker': ['aaa', 'bbb', 'ccc']})
# #     currentQty = currentQty.set_index('ticker')

# #     # setup portfolio
# #     p = pf.Portfolio()
# #     p.setCurrent(currentQty,100)
# #     prevTotal = p.getCashValue() + p.getStocksValue()

# #     # set changes
# #     changesQty = pd.DataFrame( {
# #         "chgTicker": ['bbb'],
# #         "chgQty": [50]} )
# #     changesQty = changesQty.set_index('chgTicker')   
# #     p.applyChanges(changesQty)

    
# #     c = p.getCurrent()

# #     assert c['qty']['bbb'] == 90

# #     currTotal = p.getCashValue() + p.getStocksValue()
# #     assert currTotal == prevTotal



# def test_rebalance():

#     '''
#     test data
#     ''' 
   
#     #  what we have
#     currentQty = pd.read_csv('test/test_current.csv',\
#                     dtype={'ticker': np.str_, 'qty': np.int_},\
#                     index_col='ticker'
#                         )
#     cash = 600000

#     #  what we want
#     tgtPercentage = pd.read_csv('test/test_imoex.csv',\
#                     dtype={'ticker': np.str_, 'percent': np.float64},\
#                     index_col='ticker'
#                         )

#     '''
#     setup
#     '''

#     p = pf.Portfolio()
#     p.setTarget(tgtPercentage)
#     p.setCurrent(currentQty,cash)

#     s1 = p.getStd()
#     c1 = p.getCashValue()
#     a1 = p.getStocksValue()

#     '''
#     assertions
#     '''
    
#     c = p.rebalance()
#     p.applyChanges(c)

#     s2 = p.getStd()
#     c2 = p.getCashValue()
#     a2 = p.getStocksValue()

#     # assert s2 < s1
#     # assert c2 < c1
#     # assert a2 > a1


# # def test_rebalance_positive():

# #     '''
# #     test data
# #     ''' 
   
# #     #  what we have
# #     currentQty = pd.read_csv('test/test_current.csv',\
# #                     dtype={'ticker': np.str_, 'qty': np.int_},\
# #                     index_col='ticker'
# #                         )
# #     cash = 1000

# #     #  what we want
# #     tgtPercentage = pd.read_csv('test/test_imoex.csv',\
# #                     dtype={'ticker': np.str_, 'percent': np.float64},\
# #                     index_col='ticker'
# #                         )

# #     '''
# #     setup
# #     '''

# #     p = pf.Portfolio()
# #     p.setTarget(tgtPercentage)
# #     p.setCurrent(currentQty,cash)

# #     s1 = p.getStd()
# #     c1 = p.getCashValue()
# #     a1 = p.getStocksValue()

# #     '''
# #     assertions
# #     '''
    
# #     c = p.rebalance()
# #     # display(c)
# #     assert c['chgValue'].sum()<cash
# #     assert len(c[c['chgValue']<0]) == 0