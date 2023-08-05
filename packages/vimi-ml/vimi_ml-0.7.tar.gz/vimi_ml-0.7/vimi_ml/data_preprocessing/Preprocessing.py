import pandas as pd
import numpy as np

def preprocessing(df):
    """ Return X_train, X_test, y_train, y_test """
    # import csv file with the data in it
    #dframe = pd . read_csv ('NIBanodes.csv ', encoding ='cp1252 ')
    dframe= df

    # rename the unnamed column to Unknown
    dframe.rename(columns ={'Unnamed:0': 'Unknown'}, inplace = True )

    # drop the four unnecessary columns for any data analysis
    #dframe = dframe.drop(['DOI', 'Title', 'Unknown', 'Year'] , axis = 1)
    dframe = dframe.drop(['DOI', 'Title', 'Unknown', 'Year', 'electrode_composition'] , axis = 1)

    # drop the columns that are unrelated to rate retention experiments
    dframe = dframe.drop(['cycles', 'CE_first_cycle', 'current_long_cycling', 'capacity_at_end', 'capacity_retention'] , axis = 1)


    #go through each column and drop any of those that contain more than the threshold allowed missing information
    threshold = 338
    dropl = []
    for i in range(0, len(dframe.columns), 1):
        x = dframe.iloc[: , i ].isnull().sum()
        if x > threshold:
            dropl.append(list(dframe.columns)[i])
        dframed = dframe.drop(dropl ,axis =1).dropna()

    # drop any columns that have excessive rate_retention values since those are errors in data collection
    dframed = dframed[dframed['rate_retention'] < 1.1]

    # ensure that the lower voltage column is all of a numeric datatype , rather than strings
    dframed['lower voltage'] = pd.to_numeric(dframed['lower voltage'], errors ='coerce')
    dframed = dframed.dropna()
    
    # Y Data
    y_data= (dframed['rate_retention'])
    
    # X Data
    dframed= dframed.drop(['rate_retention'], axis =1)
    
    # Label Encoder
    from sklearn . preprocessing import OneHotEncoder , LabelEncoder
    le = LabelEncoder()
    ohe =  OneHotEncoder()
    
    x_data_le = dframed[list( dframed[dframed.T[dframed.dtypes == np.object].index].columns)].apply(le.fit_transform)
    
    # One Hot Encoder
    ohe_columnval = list (dframed[dframed.T[dframed.dtypes == np.object].index ].columns)
    x_data_ohe= pd.get_dummies(dframed, columns = ohe_columnval)
    
    # Splitting the dataset into the Training set and Test set
    from sklearn.model_selection import train_test_split
    X_train, X_test, y_train, y_test = train_test_split(x_data_ohe, y_data, test_size = 0.2, random_state = 0)
    
    return X_train, X_test, y_train, y_test;