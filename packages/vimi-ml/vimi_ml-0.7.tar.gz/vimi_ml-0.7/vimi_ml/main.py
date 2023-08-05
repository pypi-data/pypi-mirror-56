# Import Libraries
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
import ast
from matplotlib import pyplot as plt
import pickle

# Read Input Configuration
from read_input import ReadInput

# Data Preprocessing Module
from vimi_ml.data_preprocessing.handle_missing import MissingValues
from vimi_ml.data_preprocessing.remove_outliers import Outliers
from vimi_ml.data_preprocessing.remove_constant_columns import ConstantColumns
from vimi_ml.data_preprocessing.normalize_numerical_columns import Standardize
from vimi_ml.data_preprocessing.encode_categorical_data import Encode

# sklearn regression models
from sklearn.linear_model import *
from sklearn.ensemble import *

#sklearn classification models
from sklearn.neural_network import MLPClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.gaussian_process import GaussianProcessClassifier
from sklearn.gaussian_process.kernels import RBF
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.discriminant_analysis import QuadraticDiscriminantAnalysis

# Hyperparamter Optimization Module
from hyperparamter_optimization import HyperparameterOptimization

# Visualization Module
from plot import PredictionPlot, Histogram, ScatterPlotMatrix, bar


###############################################################################
############################ Regression Model #################################
###############################################################################
def reg_main(model_configurations, data_filename):
    
    #############################################################################
    ##################### Read Input: model_configurations ######################
    #############################################################################
    config = ReadInput.read_input(model_configurations)
    # Input Features
    input_features = config['input_features']
    # Target Feature
    target_feature = config['target_feature']
    # Model: model name as a string, eg, model= 'LinearRegression'
    model = config['model']
    
    # convert model string to model object/class, eg, model= 'LinearRegression' to model= LinearRegression
    model = 'model= '+model
    def foo(model):
        ldict = {}
        exec(model,globals(),ldict)
        a = ldict['model']
        return a
    model = foo(model) 
    
    # Model's Hyperapameters, eg, hyperparameters = {'param_num': [0,100], 'param_str': ['str1', 'str2', 'str3']}
    hyperparameters = config['hyperparameters']
    # Data Preprocess
    data_preprocess = config['data_preprocess']
    # Plots
    plots = config['plots']
    ###############################################################################
    ############################ 1. Read Data #####################################
    ###############################################################################
    # Read Filename
    try:
        # read csv
        df= pd.read_csv(data_filename, encoding ='latin1')
    except:
        # read excel
        df= pd.read_excel(data_filename)
    ###############################################################################
    ############################ 2. Data Preprocess ###############################
    ###############################################################################
    ############################## Import Class ###################################
    # Handle Missing Values
    missing_values = MissingValues()
    missing_values.strategy = data_preprocess['MissingValue']

    # Remove Outliers
    remove_outliers = Outliers()

    # Remove Constant Columns    
    remove_constant_columns = ConstantColumns()

    # Standardize Numerical Data
    normalize_numerical_columns = Standardize()
    normalize_numerical_columns.strategy = data_preprocess['Standardize']

    # Encode Categorical Data
    encode_categorical_data = Encode()
    encode_categorical_data.strategy = data_preprocess['Encode']
    
    ####################################### Preprocess #############################
    # Handle Missing Values
    df = missing_values.fit_transform(df)
    
    # Remove Constant Columns   
    if data_preprocess['RemoveConstantColumns'] == True:
        df = remove_constant_columns.fit_transform(df)
        
    # Remove Outliers
    if data_preprocess['RemoveOutliers'] == True:
        df = remove_outliers.fit_transform(df)
        
    # Standardize Numerical Data
    # normalize_numerical_columns.strategy = 'MinMax'
    df = normalize_numerical_columns.transform(df)
    
    # Encode Categorical Data
    df_scatter = df.copy()
    df = encode_categorical_data.transform(df)
    ###############################################################################
    ############################ 3. Test-Train Split ##############################
    ###############################################################################
    # Separate Input and Target Features
    columns = list(df)

    # Target Feature
    y_columns = target_feature

    # Input Features
    if input_features == ['Auto']:
        x_columns = list(set(columns)-set(y_columns))
    else:
        x_columns = input_features

    # Input and target Data    
    x = df[x_columns]
    y = df[y_columns]

    # Test-Train Split
    X_train, X_test, y_train, y_test = train_test_split(x, y, test_size = 0.2, random_state = 0)
    print(X_train)

    # Convert y_train and y_test to data arrays
    y_train = np.ravel(y_train)
    y_test = np.ravel(y_test)
    ###############################################################################
    ############ 4. Model Building (with Hyperparamter Optimization) ##############
    ###############################################################################
    # Model
    model = model
    param_dict = hyperparameters
    
    # Model Paramter Tuning
    tune = HyperparameterOptimization(model= model,  param_dict= param_dict)

    # returns model and best hyperparamter values
    model, best_parameters = tune.hyperopt(X_train, y_train)
    
    # fit model
    model.fit(X_train, y_train)
    ###############################################################################
    ############################### 5. Predict and Error ##########################
    ###############################################################################
    y_predict= model.predict(X_test)
    from sklearn.metrics import mean_squared_error
    mse =  mean_squared_error(y_test, y_predict)
    

    ###############################################################################
    ############################### 6. Visualize ##################################
    ###############################################################################
    # Plot Histogram
    if 'Histogram' in plots:
        histogram_plot = Histogram().plot(y)
        #show(histogram_plot)
        # save plot
        histogram_plot.savefig('Histogram.png')
    plt.clf()    
    # Plot Scatter Plot Matrix
    if 'Scatter Matrix Plot' in plots:
        scatter_plot = ScatterPlotMatrix().plot(df_scatter)
        # save plot
        scatter_plot.savefig('ScatterMatrixPlot.png')
    plt.clf()    
    # Plot Prediction Plot
    y_train_pred = model.predict(X_train)
    if 'Prediction Plot' in plots:
        prediction_plot = PredictionPlot().plot(X_train, y_train, y, y_test, y_predict, y_train_pred)
        # save plot
        prediction_plot.savefig('PredictionPlot.png')
    ###############################################################################    
    ############################ 7. Create HTML File ##############################
    ###############################################################################
    # Create HTML File:
    # start html
    html_str = """
                    <!DOCTYPE html>
                    <html>
                    <body>
                    """
    # add histogram to html
    if 'Histogram' in plots:
        html_str = html_str +"""<h1>Target Histogram</h1>
                                <img src="Histogram.png">"""
    # add scatter matrix plot to html 
    if 'Scatter Matrix Plot' in plots:
        html_str = html_str +"""<h1>Scatter Matrix Plot</h1>
                                <img src="ScatterMatrixPlot.png">"""
        
    # Model used
    html_str = html_str +"""<h1>Model Used:</h1>
                    <h2>""" +config['model']+"""</h2>"""
    
    # add scatter matrix plot to html
    if 'Prediction Plot' in plots:
        html_str = html_str +"""<h1>Prediction Plot</h1>
                                <img src="PredictionPlot.png">"""
    # add prediction error to html
    html_str = html_str +"""<h1>Mean Squared Error</h1>
                        <p>""" +str(mse)+"""</p>"""
    
    # end html
    html_str = html_str+"""</body>
                            </html>"""



    Html_file= open("results.html","w")
    Html_file.write(html_str)
    Html_file.close()
    

    Html_file= open("results.html","w")
    Html_file.write(html_str)
    Html_file.close()
    
    # Save HTML to PDF
    # import pdfkit
    # pdfkit.from_file('results.html', 'results.pdf')
    
    
    ###############################################################################
    ############################## Return #########################################
    ###############################################################################
    return model




###############################################################################
########################## Classification Model ###############################
###############################################################################