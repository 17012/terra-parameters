import pandas as pd
import numpy as np
import json
import ast

rates = pd.read_csv('./reserve_luna_usd.csv', index_col=0)


def get_uluna(x):
    res = ast.literal_eval(x)
    result = res['result']
    c = list(filter(lambda rate: rate['denom'] == 'uluna', result))
    return c[0]['amount']


def get_uusd(x):
    res = ast.literal_eval(x)
    result = res['result']
    c = list(filter(lambda rate: rate['denom'] == 'uusd', result))
    return c[0]['amount']


uluna = rates['result'].apply(lambda x: get_uluna(x))
uusd = rates['result'].apply(lambda x: get_uusd(x))
newdf = pd.DataFrame({'height': rates['height'], 'uluna': uluna, 'uusd': uusd})

newdf.to_csv('reserve.csv', index=False)
