from builtins import range
import numpy as np
import pandas as pd
from sklearn import preprocessing

class Standardize(object):
    """
    Standardize all columns where the values are numerical.

    Parameters
    ----------
    strategy: string, optional (default='normalize')
        available options: 'normalize', 'scale', and 'standardize'
        Values of each column will be standardized based on the choosen strategy.
    """
    def __init__(self, strategy='normalize'):
        self.strategy = strategy
    
#     def find_columns(df):
#         """
#         Find the columns for normalization
        
#         Parameters
#         ----------
#         df: pandas dataframe
#             input dataframe

#         Returns
#         -------
#         A list of column names
#         """
#         standardize_columns
    
    def transform(self, df):
        """
        Standardize columns that are in the encode_columns attribute of the previous find_columns method

        Parameters
        ----------
        df: pandas dataframe
            input dataframe

        Returns
        -------
        transformed dataframe
        """
    
        if self.strategy == 'normalize':
             


            numeric_data= df.select_dtypes(include=['float64', 'int64']) #DataFrame withonly numeric data
            x = numeric_data.values #returns a numpy array with numerical data
           
            #norm = preprocessing.normalize()
            x_scaled = preprocessing.normalize(x, norm= 'l2', axis= 0)
            normalized_data = pd.DataFrame(x_scaled, columns=numeric_data.columns)
            df.update(normalized_data) #updates the original DataFrame with updated column values
            return df
        
        elif self.strategy == 'scale':

            numeric_data= df.select_dtypes(include=['float64', 'int64']) #DataFrame withonly numeric data
            x = numeric_data.values #returns a numpy array with numerical data                                       
            x_scaled = preprocessing.scale(x)
            normalized_data = pd.DataFrame(x_scaled, columns=numeric_data.columns)
            df.update(normalized_data) #updates the original DataFrame with updated column values
            return df
        

        
        elif self.strategy == 'MinMax':
            norm_data = df.copy()
            numeric_data= norm_data.select_dtypes(include=['float64', 'int64']) #DataFrame withonly numeric data
            x = numeric_data.values #returns a numpy array with numerical data
            #print(x)
           
            min_max_scaler = preprocessing.MinMaxScaler()
            x_scaled = min_max_scaler.fit_transform(x)
    
            normalized_data = pd.DataFrame(x_scaled, columns=numeric_data.columns)
        
            norm_data.update(normalized_data) #updates the original DataFrame with updated column values
            norm_data1=norm_data
            return norm_data1