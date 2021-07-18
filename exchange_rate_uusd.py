import pandas as pd
import numpy as np
import json
import ast

rates = pd.read_csv('./exchange_rates.csv', index_col=0)


def get(x):
    res = ast.literal_eval(x)
    result = res['result']
    c = list(filter(lambda rate: rate['denom'] == 'uusd', result))
    return c[0]['amount']


rates['result'] = rates['result'].apply(lambda x: get(x))

rates.to_csv('uusd_rate.csv', index=False)
