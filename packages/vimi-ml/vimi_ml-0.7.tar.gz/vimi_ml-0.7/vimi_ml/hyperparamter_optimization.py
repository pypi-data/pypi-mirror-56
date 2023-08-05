import pandas as pd
import numpy as np



class HyperparameterOptimization(object):
    
    """
    outputs the optimized values of the hyperparameter of a machine learning model.
    The optimized values are the tuned values according to a dataset.
    
    Parameters:
    ---------------------
    
    
    """
    
    
    def __init__(self,model,
                 param_dict,
                 max_evals= 100,
                 cv_folds= 5,
                 scoring= 'neg_mean_squared_error'):
        
        self.model = model
        self.param_dict = param_dict
        self.max_evals = max_evals
        self.cv_folds = cv_folds
        self.scoring = scoring
        
        

    def hyperopt(self, X_train, y_train):
        model = self.model
        hyperparameter_dictionary = self.param_dict


        
        if len(hyperparameter_dictionary)>=1:
                
            #####################################################################################################
            ########### Separating Hyperparameter Names and Values from Hyperparameter Dictionary ###############
            #####################################################################################################

            # Getting List of hyperparamter names from hyperparamter_dictionary
            hyperparameter_name_list= list(hyperparameter_dictionary.keys())

            # Getting List of hyperparamter values from hyperparamter_dictionary
            hyperprameter_value_list= [];
            for key in list(hyperparameter_dictionary): 
                hyperprameter_value_list.append(hyperparameter_dictionary[key])
                
        ######################################################################################################
        ####################################### 1. Objective Function ########################################
        ######################################################################################################
        scores= [];
        def objective(hyperparameters):
            """
            Objective function to minimize error.
            Returns validation score from hyperparameters.
            """
            print(hyperparameters)
            
#             # Make Hyperparameter Dictionary
#             hyp_dict = {}
#             for i in range(len(hyperparameter_name_list)):
#                     if(type(hyperparameter_dictionary[hyperparameter_name_list[i]][0])== int):
#                         hyp_dict[hyperparameter_name_list[i]] = int(hyperparameters[i])
#                     else:
#                         hyp_dict[hyperparameter_name_list[i]] = (hyperparameters[i])
                        
            try:
                for key in (hyperparameters):
                    if type(hyperparameters[key]) == float:
                        if hyperparameters[key]/int(hyperparameters[key]) == 1.0:
                            hyperparameters[key] = int(hyperparameters[key])
            except:
                pass
            # Model            
            model = self.model(**hyperparameters)

            # Cross validating the model with training data
            from sklearn.model_selection import cross_validate
            cv_results = cross_validate(model, X_train, y_train, cv=self.cv_folds, scoring= self.scoring)

            # Taking average score from cross validating result
            score= -1*np.mean(cv_results['test_score'])
            
            scores.append(score)
            return score
       #######################################################################################################
        ###################################### 2. Domain Space ################################################
        #######################################################################################################
        from hyperopt import hp
        space = {}
        for i in range(len(hyperparameter_name_list)):
            # String Value
            if(type(hyperparameter_dictionary[hyperparameter_name_list[i]][0])==str or type(hyperparameter_dictionary[hyperparameter_name_list[i]][0])==bool):
                space[hyperparameter_name_list[i]] = hp.choice(hyperparameter_name_list[i], hyperparameter_dictionary[hyperparameter_name_list[i]])
            # Integer Value
            elif(type(hyperparameter_dictionary[hyperparameter_name_list[i]][0])==int):
                space[hyperparameter_name_list[i]] = hp.quniform(hyperparameter_name_list[i], hyperparameter_dictionary[hyperparameter_name_list[i]][0], hyperparameter_dictionary[hyperparameter_name_list[i]][1], 1)
            # Floating Value
            elif(type(hyperparameter_dictionary[hyperparameter_name_list[i]][0])==float):
                space[hyperparameter_name_list[i]] = hp.uniform(hyperparameter_name_list[i], hyperparameter_dictionary[hyperparameter_name_list[i]][0], hyperparameter_dictionary[hyperparameter_name_list[1]])


        ########################################################################################################
        ################################### 3. Optimization Algortihm ##########################################
        ########################################################################################################
        from hyperopt import tpe
        # Create the algorithm
        tpe_algo = tpe.suggest

        ########################################################################################################
        ######################################### 4. Results ###################################################
        ########################################################################################################
        from hyperopt import Trials
        # Create a trials object
        tpe_trials = Trials()

        ########################################################################################################
        ######################################## 5. Optimization ###############################################
        ########################################################################################################

        from hyperopt import fmin
        # Run 200 evals with the tpe algorithm
        tpe_best = fmin(fn=objective, space=space, 
                        algo=tpe_algo, trials=tpe_trials,
                        max_evals= self.max_evals)
        print(tpe_best)


#         import matplotlib.pyplot as plt
#         plt.figure(num=None, figsize=(8, 6))
#         plt.plot(scores, 'r-')
#         plt.xlabel('Number of Itteration')
#         plt.ylabel('Average Cross Validation Score')


        #########################################################################################################
        ################################### 6. Final Optimized Model ############################################
        #########################################################################################################


        # Putting the arguements for the machine learning model into one string
                # Make Hyperparameter Dictionary
        hyp_dict = {}
        for i in range(len(hyperparameter_name_list)):
                if(type(hyperparameter_dictionary[hyperparameter_name_list[i]][0])== int):
                    hyp_dict[hyperparameter_name_list[i]] = int(tpe_best[hyperparameter_name_list[i]])

                elif(type(hyperparameter_dictionary[hyperparameter_name_list[i]][0])== bool):
                    if str((tpe_best[hyperparameter_name_list[i]]))=='1':
                        hyp_dict[hyperparameter_name_list[i]] = True
                    else:
                        hyp_dict[hyperparameter_name_list[i]]  = False
                        
                elif(type(hyperparameter_dictionary[hyperparameter_name_list[i]][0])== str) and (type(tpe_best[hyperparameter_name_list[i]])==int or type(tpe_best[hyperparameter_name_list[i]])==float):
                    hyp_dict[hyperparameter_name_list[i]] = hyperparameter_dictionary[hyperparameter_name_list[i]][tpe_best[hyperparameter_name_list[i]]]
                        
                else:
                    hyp_dict[hyperparameter_name_list[i]] = (tpe_best[hyperparameter_name_list[i]])
        # Model
        for key in (hyp_dict):
            if type(hyp_dict[key]) == float:
                if hyp_dict[key]/int(hyp_dict[key]) == 1.0:
                    hyp_dict[key] = int(hyp_dict[key])
        print(type(hyperparameter_dictionary[hyperparameter_name_list[i]][0]),type(tpe_best[hyperparameter_name_list[i]]))
        print(hyp_dict)
                    
        model = self.model(**hyp_dict)
        
        # Return Optimized model and Optimized values for hyperparameters
        return model, hyp_dict


    

        