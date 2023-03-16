from .lispy import make_interpreter, s
import pandas as pd
import numpy as np

# class Arguments(object):

#     df = "df"
#     column_name = "column_name"
#     of_type = "of_type"

# class TransformType(object):

#     column = "column"
#     multi_column = "multi_column"
#     shape_change = "shape_change"

# class FillNAC(Transform):
#     @staticmethod 
#     def transform(df, col, val):
#         df.fillna({col:val}, inplace=True)
#         return df

#     @staticmethod 
#     def transform_to_py(df, col, val):
#         return "    df.fillna({'%s':%r}, inplace=True)" % (col, val)

# class OneHotC(Transform):
#     @staticmethod 
#     def transform(df, col, val):
#         one_hot = pd.get_dummies(df[col])
#         df = df.drop(col, axis=1, inplace=True)
#         #how to make this inplace?
#         return df.join(one_hot) 

#     @staticmethod 
#     def transform_to_py(df, col, val):
#         commands = [
#             "    one_hot = pd.get_dummies(df['%s'])" % (col),
#             "    df.drop('%s', inplace=True)" % (col),
#             "    df = df.join(one_hot)"]
#         return "\n".join(commands)
#     arguments = [Arguments.df, Arguments.column_name]
#     command_template = [s('make-categorical'), s('df'), "col"]




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


def configure_dcf(transforms):
    command_defaults = {}
    command_patterns = {}

    transform_lisp_primitives = {}
    to_py_lisp_primitives = {}
    for T in transforms:
        t = T()
        transform_name = t.command_default[0]['symbol']
        command_defaults[transform_name] = t.command_default
        command_patterns[transform_name] = t.command_pattern
        transform_lisp_primitives[transform_name] = T.transform
        to_py_lisp_primitives[transform_name] = T.transform_to_py
    
    dcf_eval, raw_parse = make_interpreter(transform_lisp_primitives)
    def dcf_transform(instructions, df):
        df_copy = df.copy()
        return dcf_eval(instructions, {'df':df_copy})

    convert_to_python, __unused = make_interpreter(to_py_lisp_primitives)
    def dcf_to_py(instructions):
        #I would prefer to implement this with a macro named something
        #like 'clean' that is implemented for the _convert_to_python
        #interpreter to return a string code block, and for the real DCF
        #interpreter as 'begin'... that way the exact same instructions
        #could be sent to either interpreter.  For now, this will do
        individual_instructions =  [x for x in map(lambda x:convert_to_python(x, {'df':5}), instructions)]
        code_block =  '\n'.join(individual_instructions)

        return "def clean(df):\n" + code_block
    return command_defaults, command_patterns, dcf_transform, dcf_to_py

command_defaults, command_patterns, dcf_transform, dcf_to_py_core = configure_dcf([
    FillNA, DropCol, OneHot])

    

# class MakeCategorical(Transform):
#     t_type = TransformType.column
#     arguments = [Arguments.df, Arguments.column_name]
#     command_template = [s('make-categorical'), s('df'), "col"]
    


