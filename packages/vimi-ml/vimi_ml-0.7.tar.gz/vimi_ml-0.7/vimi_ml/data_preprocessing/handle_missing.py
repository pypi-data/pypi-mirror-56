import warnings
from builtins import range

import pandas as pd
import numpy as np

# from validation import check_object_col


class MissingValues(object):
    """
    find missing values and interpolate/replace or remove them.

    Parameters
    ----------
    strategy: string, optional (default="ignore_row")
        
        list of strategies:
        - interpolate: interpolate based on sorted target values
        - zero: set to the zero
        - ignore_row: remove the entire row in data and target
        - ignore_column: remove the entire column in data and target

    string_as_null: boolean, optional (default=True)
        If True non numeric elements are considered to be null in computations.
    
    missing_values: list, optional (default=None)
        where you define specific formats of missing values. It is a list of string, float or integer values.

    inf_as_null: boolean, optional (default=True)
        If True inf and -inf elements are considered to be null in computations.

    columns : list of variable names, optional (default = 'all')
        Variables within data to use, otherwise use every column with a numeric datatype.


    Returns
    -------
    data frame
    mask: Only if strategy = ignore_row. Mask is a binary pandas series which stores the information regarding removed
    """

    def __init__(self,
                 strategy="ignore_row",
                 string_as_null=True,
                 inf_as_null=True,
                 missing_values=None,
                 columns= 'all'):
        self.strategy = strategy
        self.string_as_null = string_as_null
        self.inf_as_null = inf_as_null
        self.missing_values = missing_values
        self.columns = columns

    def fit_transform(self, df):
        """
        use fit_transform for:
            - replace missing values with nan.
            - drop columns with all nan values.
            - fill nan values with the specified strategy.

        Parameters
        ----------
        df : pandas data frame

        Attributes
        ----------
        binary pandas series, only if strategy = 'ignore_row' or 'ignore_column'
            mask is a binary vector whose length is the number of rows/indices in the df. The index of each bit shows
            if the row/column in the same position has been removed or not.
            The goal is keeping track of removed rows/columns to change the target data frame or other input data frames based
            on that. The mask can later be used in the transform method to change other data frames in the same way.
        """
        columns = list(df)
        not_columns = []
        df_not = df[not_columns]
        
        if self.columns != 'all':
            not_columns = list(set(columns)-set(self.columns))
            df_not = df[not_columns]
            df = df[self.columns]


        # Separating"Numeric" and "Object" columns
        df_object = df.select_dtypes(include=['object'])
        df = df.select_dtypes(include=['float64', 'int64'])
        
        
        if self.inf_as_null == True:
            df.replace([np.inf, -np.inf, 'inf', '-inf'], np.nan, True)
        if self.string_as_null == True:
            for col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='ignore') # from 'coerce' to 'ignore'
        if isinstance(self.missing_values, (list, tuple)):
            for pattern in self.missing_values:
                df.replace(pattern, np.nan, True)
                
        #print(len(df))
        
        #df = check_object_col(df, 'df')

        #print(list(df))
        # drop null columns
        df.dropna(axis=1, how='all', inplace=True)

        #print(list(df))

        if self.strategy == 'zero':
            for col in df.columns:
                df[col].fillna(value=0, inplace=True)
                
            List = list(df.index)
            df_object = df_object.loc[List]
            df = pd.merge(df, df_object, left_index = True, right_index = True)
            df = pd.merge(df, df_not, left_index = True, right_index = True)
            return df
        elif self.strategy == 'ignore_row':
            dfi = df.index
            df.dropna(axis=0, how='any', inplace=True)
            print(list(df))
            mask = [i in df.index for i in dfi]
            self.mask = pd.Series(mask, index=dfi)
            # self.mask = pd.notnull(df).all(1)
            # df = df[self.mask]
            List = list(df.index)
            df_object = df_object.loc[List]
            df = pd.merge(df, df_object, left_index = True, right_index = True)
            df = pd.merge(df, df_not, left_index = True, right_index = True)
            df = df.reset_index(drop = True)
            return df
        elif self.strategy == 'ignore_column':
            dfc = df.columns
            df.dropna(axis=1, how='any', inplace=True)
            mask = [i in df.columns for i in dfc]
            self.mask = pd.Series(mask, index=dfc)
            
            List = list(df.index)
            df_object = df_object.loc[List]
            df = pd.merge(df, df_object, left_index = True, right_index = True)
            df = pd.merge(df, df_not, left_index = True, right_index = True)
            # self.mask = pd.notnull(df).all(0)
            # df = df.T[self.mask].T
            return df
        elif self.strategy == 'interpolate':
            df = df.interpolate()
            df.fillna(
                method='ffill', axis=1, inplace=True
            )  # because of nan in the first and last element of column
            
            List = list(df.index)
            df_object = df_object.loc[List]
            df = pd.merge(df, df_object, left_index = True, right_index = True)
            df = pd.merge(df, df_not, left_index = True, right_index = True)
            return df
        else:
            msg = "Wrong strategy has been passed"
            raise TypeError(msg)

    def transform(self, df):
        """
        Only if the class is fitted with 'ignore_row' or 'ignore_column' strategies.

        Parameters
        ----------
        df : pandas dataframe

        Returns
        -------
        transformed data frame based on the mask vector from fit_transform method.
        """
        if self.strategy == 'ignore_row':
            return df[self.mask]
        elif self.strategy == 'ignore_column':
            return df.loc[:, self.mask]
        else:
            msg = "The transform method doesn't change the dataframe if strategy='zero' or 'interpolate'. You should fit_transform the new dataframe with those methods."
            warnings.warn(msg)