import pandas as pd
import numpy as np
from .lispy import make_interpreter, s
import json

def dropcol(df, col):
    df.drop(col, axis=1, inplace=True)
    return df

def fillna(df, col, val):
    df.fillna({col:val}, inplace=True)
    return df


sample_df = pd.DataFrame({'a':[2,None], 'b':['3', 'a'], 'c':[5, None]})

def test_dropcol():
    dropped_df = dropcol(sample_df.copy(), 'b')
    assert dropped_df is not sample_df
    #I want to make sure we haven't modified df
    assert len(dropped_df.columns) != len(sample_df.columns)
    assert 'b' not in dropped_df.columns


def test_fillna():
    filled_df = fillna(sample_df.copy(), 'a', 13)

    assert filled_df is not sample_df
    assert np.isnan(sample_df.iloc[1]['a'])
    assert np.isnan(sample_df.iloc[1]['c'])
    assert np.isnan(filled_df.iloc[1]['c'])
    assert filled_df.iloc[1]['a'] == 13


_eval = make_interpreter({'dropcol':dropcol, 'fillna':fillna})
def dcf_transform(instructions, df):
    df_copy = df.copy()
    return _eval(instructions, {'df':df_copy})

def test_interpret_fillna():
    # I would like to have symbol:df be implicit,  I can do that later
    filled_df = dcf_transform(
        [s('fillna'), s('df'), 'a', 13], sample_df)
    assert filled_df is not sample_df
    assert np.isnan(sample_df.iloc[1]['a'])
    assert np.isnan(sample_df.iloc[1]['c'])
    assert np.isnan(filled_df.iloc[1]['c'])
    assert filled_df.iloc[1]['a'] == 13

                              
def test_interpret_dropcol():
    # I would like to have symbol:df be implicit,  I can do that later
    dropped_df = dcf_transform(
        [s('dropcol'), s('df'), 'b'], sample_df)
    assert dropped_df is not sample_df
    #I want to make sure we haven't modified df
    assert len(dropped_df.columns) != len(sample_df.columns)
    assert 'b' not in dropped_df.columns

def test_interpret_multiple_dropcol():
    # I would like to have symbol:df be implicit,  I can do that later
    dropped_df = dcf_transform([
        s('begin'), 
        [s('dropcol'), s('df'), 'b'],
        [s('dropcol'), s('df'), 'c']],
                               sample_df)


    # [
    #     {"symbol":"begin"},[[{"symbol":"dropcol"},{"symbol":"df"},"tripduration"]]]
    assert dropped_df is not sample_df
    #I want to make sure we haven't modified df
    assert len(dropped_df.columns) != len(sample_df.columns)
    assert 'b' not in dropped_df.columns
    assert 'c' not in dropped_df.columns


print(json.dumps([s('dropcol'), s('df'), 'b']))

    
def dropcol_py(df, col):
    return "    df.drop(%s, axis=1, inplace=True)" % col

def fillna_py(df, col, val):
    return "    df.fillna({'%s':%r}, inplace=True)" % col, val


_convert_to_python = make_interpreter({'dropcol':dropcol_py, 'fillna':fillna_py})

def dcf_to_py(instructions):
    individual_instructions =  [x for x in map(lambda x:_convert_to_python(x, {'df':5}), instructions)]
    return '\n'.join(individual_instructions)


def test_to_py():
    assert dcf_to_py([[s('dropcol'), s('df'), 'b'],
                      [s('dropcol'), s('df'), 'c']]) == "foo"
