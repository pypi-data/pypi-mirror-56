from builtins import range
import numpy as np
import pandas as pd


class ConstantColumns(object):
    """
    remove constant columns


    Attributes
    ----------
    removed_columns: list of column headers that have been removed

    Returns
    -------
    df: pandas dataframe

    """

    def fit_transform(self, df):
        """
        fit the method to the input dataframe and change it accordingly

        Parameters
        ----------
        df: pandas dataframe
            input dataframe

        Returns
        -------
        transformed dataframe
        """
        dfc = df.columns
        df = df.loc[:, (df != df.iloc[0]).any()]
        self.removed_columns_ = np.array(
            [i for i in dfc if i not in df.columns])
        return df

    def transform(self, df):
        """
        find and remove headers that are in the removed_columns_ attribute of the previous fit_transform method

        Parameters
        ----------
        df: pandas dataframe
            input dataframe

        Returns
        -------
        transformed dataframe
        """
        df = df.drop(self.removed_columns_, 1)
        return df


