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

group_df = pd.DataFrame({'a':[10,20,30,40,50,60],
                   'b':[1,2,3,4,5,6],
                   'c':['q', 'q', 'q', 'q', 'w', 'w']})



class GroupBy(Transform):
    command_default = [s("groupby"), s('df'), 'col', {}]
    command_pattern = [[3, 'colMap', 'colEnum', ['null', 'sum', 'mean', 'count']]]
    @staticmethod 
    def transform(df, col, col_spec):
        grps = df.groupby(col)
        df_contents = {}
        for k, v in col_spec.items():
            if v == "sum":
                df_contents[k] = grps[k].apply(lambda x: x.sum())
            elif v == "mean":
                df_contents[k] = grps[k].apply(lambda x: x.mean())
        #print(df_contents)
        return pd.DataFrame(df_contents)

    test_df = group_df
    test_sequence = [s("groupby"), s('df'), 'c', dict(a='sum', b='mean')]
    test_output = pd.DataFrame(
        {'a':[100, 110], 'b':[2.5, 5.5]},
        index=['q','w'])

    @staticmethod 
    def transform_to_py(df, col,colspec):
        commands = [
            "    col " % (col),
            "    colspec %r " % (colspec)]
        return "\n".join(commands)
    



command_defaults, command_patterns, dcf_transform, dcf_to_py_core = configure_dcf([
    FillNA, DropCol, OneHot, GroupBy])
#print(GroupBy.test_output)
print(dcf_transform(GroupBy.test_sequence, GroupBy.test_df))


# class MakeCategorical(Transform):
#     t_type = TransformType.column
#     arguments = [Arguments.df, Arguments.column_name]
#     command_template = [s('make-categorical'), s('df'), "col"]
    


