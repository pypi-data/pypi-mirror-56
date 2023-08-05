import pandas as pd
import numpy as np
from matplotlib import pyplot as plt

import seaborn as sns
from sklearn import preprocessing


from sklearn.metrics import mean_squared_error



class PredictionPlot(object):

    def __init__(self, line_color= 'g',
                 test_color= 'b',
                 train_color= 'r'):

        self.line_color = line_color
        self.test_color = test_color
        self.train_color = train_color


    def plot(self, X_train, y_train, y_total, y_test, y_predict, y_train_pred):

        # Plot Label:
        print('MSE: '+str(mean_squared_error(y_test, y_predict)))
        #strng = 'Current Density (Normalized)'
        plt.xlabel('Actual ')
        plt.ylabel('Predicted ')

        # Plot prediction
        y_plot = np.ravel(y_total)
        plt.plot(y_plot, y_plot,self.line_color, label = 'Actual')

        # Scatter Plot: Test Predcition
        plt.scatter(y_test, y_predict,c = self.test_color, label = 'Test Data')

        # Scatter Plot: Train Prediction

        plt.scatter(y_train, y_train_pred, c = self.train_color, label = 'Train Data')

        # Show Legend
        plt.legend()

        return plt


class Histogram(object):
    """
    Histogram Plot
    """
    
    def __init__(self, bins= 20,
                 rwidth= 1,
                 color= 'green',
                 x_label= 'Value',
                 y_label= 'Frequency'):
        
        self.bins = bins
        self.rwidth = rwidth
        self.color = color
        self.x_label = 'Value'
        self.y_label = 'Frequency'
        
    def plot(self, x):
        try:
            self.x_label = list(x)[0]
            x = np.ravel(x)
        except:
            pass
            
        plt.hist(x, bins= self.bins,
                 rwidth= self.rwidth,
                 color= self.color)
        
        plt.xlabel(self.x_label)
        plt.ylabel(self.y_label)
        #plt.text(100, 50, 'test')
        return plt
    
     
class bar(object):
    """
    Bar Plot for categorical data
    
    """
    
    def __init__(self, bins= 20,
                 rwidth= 1,
                 color= 'green',
                 x_label= 'Value',
                 y_label= 'Frequency'):
        
        self.bins = bins
        self.rwidth = rwidth
        self.color = color
        self.x_label = 'Value'
        self.y_label = 'Frequency'
        
    def plot(self, df):
        a= df.value_counts()
        data = a.to_dict()
        names = list(data.keys())
        values = list(data.values())
        
        plt.bar(names, values)
        
        plt.xlabel(self.x_label)
        plt.ylabel(self.y_label)
        #plt.text(100, 50, 'test')
        return plt   
    
    
    
class ScatterPlotMatrix(object):
    """
    The scatter plot matrix plotting interface. It is built on top of the seaborn.pairplot function.
    
    Parameters
    ----------

    hue : string (variable name), optional (default = None)
        Variable in data to map plot aspects to different colors.
        
    kind : string, optional (default = 'scatter')
        available options: ‘scatter’, ‘reg’
        Kind of plot for the non-identity relationships.
    
    diag_kind : string, optional (default = 'hist')
        available options: ‘auto’, ‘hist’, ‘kde’
        Kind of plot for the diagonal subplots. The default depends on whether "hue" is used or not.
        
    markers : list of string, optional (default = 'o' (None))
        avalable option: single matplotlib marker code or list
        Either the marker to use for all datapoints or a list of markers with a length the same as the number of levels in the hue variable so that differently colored points will also have different scatterplot markers.

    vars : list of variable names, optional (default = None (All Numneric Columns))
        Variables within data to use, otherwise use every column with a numeric datatype.
        
    dropna : boolean, optional (default = True)
        available option: True, False
        Drop missing values from the data before plotting.
        
    normalize : boolean, optional (default = False)
        available option: True, False
        Weather to normlize the input dataframe.
        
    """

    def __init__(self, hue= None,
                 kind= 'scatter',
                 diag_kind= 'hist',
                 markers= None,
                 vars= None,
                 dropna= True,
                 normalize= True):
        
        self.hue = hue
        self.kind = kind
        self.diag_kind = diag_kind
        self.markers = markers
        self.vars = vars
        self.dropna = dropna
        self.normalize = normalize
        
    def plot(self, dataset):
        df = dataset.copy()
        
        """
        the main function to plot based on the input dataframe
        
        Parameters
        ----------
        df: pandas dataframe
        
        Returns
        -------
        seaborn.axisgrid.PairGrid object
        """
        if self.normalize == True:

            numeric_data= df.select_dtypes(include=['float64', 'int64']) #DataFrame withonly numeric data
            x = numeric_data.values #returns a numpy array with numerical data
            min_max_scaler = preprocessing.MinMaxScaler()
            x_scaled = min_max_scaler.fit_transform(x)
            normalized_data = pd.DataFrame(x_scaled, columns=numeric_data.columns)
            df.update(normalized_data) #updates the original DataFrame with updated column values
            df = df.dropna()
            df = df.reset_index(drop= True)
            
        
        sns.set(style="ticks", color_codes=True)
        fig = sns.pairplot(df, hue= self.hue, vars= self.vars, kind= self.kind, diag_kind= self.diag_kind, markers= self.markers, dropna= self.dropna)
        return fig