from .lispy import s
from .configure_utils import configure_dcf
import pandas as pd
import numpy as np

class Transform(object):
    pass
    
class FillNA(Transform):
    #argument_names = ["df", "col", "fill_val"]
    command_default = [s('fillna'), s('df'), "col", 8]
    command_pattern = [[3, 'fillVal', 'type', 'integer']]

    @staticmethod 
    def transform(df, col, val):
        df.fillna({col:val}, inplace=True)
        return df

    @staticmethod 
    def transform_to_py(df, col, val):
        return "    df.fillna({'%s':%r}, inplace=True)" % (col, val)

class DropCol(Transform):
    #argument_names = ["df", "col"]
    command_default = [s('dropcol'), s('df'), "col"]
    command_pattern = [None]

    @staticmethod 
    def transform(df, col):
        df.drop(col, axis=1, inplace=True)
        return df

    @staticmethod 
    def transform_to_py(df, col):
        return "    df.drop('%s', axis=1, inplace=True)" % col

class OneHot(Transform):
    command_default = [s('onehot'), s('df'), "col"]
    command_pattern = [None]
    @staticmethod 
    def transform(df, col):
        one_hot = pd.get_dummies(df[col])
        df.drop(col, axis=1, inplace=True)
        #how to make this inplace?
        return df.join(one_hot) 

    @staticmethod 
    def transform_to_py(df, col):
        commands = [
            "    one_hot = pd.get_dummies(df['%s'])" % (col),
            "    df.drop('%s', inplace=True)" % (col),
            "    df = df.join(one_hot)"]
        return "\n".join(commands)



command_defaults, command_patterns, dcf_transform, dcf_to_py_core = configure_dcf([
    FillNA, DropCol, OneHot])

    

# class MakeCategorical(Transform):
#     t_type = TransformType.column
#     arguments = [Arguments.df, Arguments.column_name]
#     command_template = [s('make-categorical'), s('df'), "col"]
    


