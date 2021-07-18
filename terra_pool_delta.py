import pandas as pd
import numpy as np
import json
import ast

rates = pd.read_csv('./terra_pool_delta.csv', index_col=0)


def get(x):
    res = ast.literal_eval(x)
    result = res['result']
    return result


rates['result'] = rates['result'].apply(lambda x: get(x))

rates.to_csv('pool_delta_final.csv', index=False)
