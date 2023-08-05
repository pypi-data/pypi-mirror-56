from builtins import range
import numpy as np
import pandas as pd

from sklearn import preprocessing

class Encode(object):
    """
    Encode all columns where the values are categorical.

    Parameters
    ----------
    strategy: string, optional (default='oneHotEncoder')
        available options: 'oneHotEncoder' and 'LabelEncoder'
        Values of each column will be encoded based on the choosen strategy.
    """
    
    def __init__(self, strategy= 'OneHotEncoder',
                 dataframe= pd.DataFrame()):
        self.strategy = strategy
        self.dataframe = dataframe
    
    
    def find_columns(df):
        """
        Find the columns for encoding
    
        Parameters
        ----------
        df: pandas dataframe
            input dataframe

        Returns
        -------
        A list of column names
        """
        return encode_columns
    
    def transform(self, df):
        """
        Encode columns that are in the encode_columns attribute of the previous find_columns method

        Parameters
        ----------
        df: pandas dataframe
            input dataframe

        Returns
        -------
        transformed dataframe
        """
        df_object = list(df.select_dtypes(include=['object']))
        df = df.dropna(how = 'any', subset = df_object)
        
        if self.strategy == 'OneHotEncoder':
            
            categorical_data = df.select_dtypes(include=['object'])
            categorical_columns = list(categorical_data)
            df = pd.get_dummies(df, columns = categorical_columns)
            return df
        
        elif self.strategy == 'LabelEncoder':
            
            categorical_data = df.select_dtypes(include=['object'])
            le = preprocessing.LabelEncoder()
            x_encoded = categorical_data.apply(le.fit_transform)
            encoded_data = pd.DataFrame(x_encoded, columns=categorical_data.columns)
            df.update(encoded_data) #updates the original DataFrame with updated column values
            return df
        
        
    def inverse_transform(self, df_dummies):

        if self.strategy == 'OneHotEncoder':
            # Original Dataframe
            df = self.dataframe.copy()

            # Numerical Columns
            numerical_columns = list(df.select_dtypes(include=['float64', 'int64']))

            # Categorical Columns List (Original)
            categorical_columns_org = list(df.select_dtypes(include=['object']))

            # Categorical Columns List (Dummies)
            categorical_columns_dum = list(df_dummies)

            # Create Dictionary with keys ad original columns names and values as dummies columns names
            column_groups = {}
            for column_org in categorical_columns_org:
                temp =[]
                for column_dum in categorical_columns_dum:
                    if column_org+'_' in column_dum:
                        temp.append(column_dum)
                column_groups[column_org] = temp

            # Create new dataframe 
            df_new = pd.DataFrame()
            for column_org in categorical_columns_org:
                df_temp = df_dummies[column_groups[column_org]]
                x = df_temp.stack()
                x= pd.Series(pd.Categorical(x[x!=0].index.get_level_values(1))).tolist()
                df_new[column_org] = x

            for columns in numerical_columns:
                df_new[columns] = df[columns]


            df_new = df_new.reset_index(drop= True)
            return df_new  
        
    