import pandas as pd
import numpy as np
from .lispy import make_interpreter

def dropcol(df, col):
    return df.drop(col, axis=1)

def fillna(df, col, val):
    return df.fillna({col:val})


sample_df = pd.DataFrame({'a':[2,None], 'b':['3', 'a'], 'c':[5, None]})

def test_dropcol():
    dropped_df = dropcol(sample_df, 'b')
    assert dropped_df is not sample_df
    #I want to make sure we haven't modified df
    assert len(dropped_df.columns) != len(sample_df.columns)
    assert 'b' not in dropped_df.columns


def test_fillna():
    filled_df = fillna(sample_df, 'a', 13)
    assert filled_df is not sample_df
    assert np.isnan(sample_df.iloc[1]['a'])
    assert np.isnan(sample_df.iloc[1]['c'])
    assert np.isnan(filled_df.iloc[1]['c'])
    assert filled_df.iloc[1]['a'] == 13

    
