# -*- coding: utf-8 -*-

"""Main module."""
from pandas import DataFrame
import pandas as pd
import sqlparse
from typing import List
Columns = List[str]


class AnalysisException(Exception):

    def __init__(self, message):

        self.message = message

    def __str__(self):

        return self.message

class DataFrame(DataFrame):

    def parse_sql_str(self,sql:str)->Columns:
        parsed_sql = sqlparse.parse(sql)
        columns = []

        if len(parsed_sql) > 0 :
            for token in parsed_sql[0].tokens:
                if token.is_keyword:
                    if token.normalized == 'SELECT':
                        pass
                if token.is_keyword== False:

                    if token.is_group and hasattr(token,'tokens'):
                        for subtoken in token.tokens:
                            if subtoken.ttype[0] == 'Name':
                                columns.append(subtoken.value)

                    if hasattr(token,'ttype'):
                        if str(token.ttype)=='Token.Wildcard':
                            columns += list(self.columns.values)
            return columns
        else:
            return columns

    def select_str(self,expression:str) -> DataFrame:
        dummy_sql = 'SELECT {0} FROM table'.format(expression)

        sql_columns = self.parse_sql_str(dummy_sql)

        selected_columns = []
        for sql_column in sql_columns:
            if sql_column in self.columns:
                selected_columns.append(sql_column)
            else:
                raise AnalysisException('cannot resolve {0} column')

        return self[selected_columns].copy()


    def select_list(self,expressions:list) -> DataFrame:
        dummy_sql = 'SELECT {0} FROM table'.format(','.join(expressions))

        sql_columns = self.parse_sql_str(dummy_sql)

        df_columns = [column for column in sql_columns if column in self.columns]

        return self[df_columns].copy()

    def select(self,*expressions):
        all_df = []
        for expression in expressions:
            if type(expression) is str:
                selected_df = self.select_str(expression)
                all_df.append(selected_df)
            elif type(expression) is list:
                selected_df = self.select_list(expression)
                all_df.append(selected_df)
            else:
                raise NotImplementedError()

        try:
            union_df = pd.concat(all_df,axis=1)
        except ValueError:
            union_df = pd.DataFrame()
        finally:
            return union_df

class column():
    def __init__(self):
        raise NotImplementedError()


class expression():
    def __init__(self):
        raise NotImplementedError()