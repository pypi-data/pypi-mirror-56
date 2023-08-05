from sklearn.linear_model import BayesianRidge
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import Ridge


class BayesianRidgeRegression(object):
    
    
    def __init__(self, n_iter=300,
                 tol=0.001,
                 alpha_1=1e-06,
                 alpha_2=1e-06,
                 lambda_1=1e-06,
                 lambda_2=1e-06,
                 compute_score=False, 
                 fit_intercept=True,
                 normalize=False,
                 copy_X=True,
                 verbose=False):
        
        
        
                 self.n_iter = n_iter
                 self.tol = tol
                 self.alpha_1 = alpha_1
                 self.alpha_2 = alpha_2 
                 self.lambda_1 = lambda_1 
                 self.lambda_2 = lambda_2
                 self.compute_score = compute_score
                 self.fit_intercept = fit_intercept 
                 self.normalize = normalize
                 self.copy_X = copy_X 
                 self.verbose = verbose 
    
    
    def fit(self, X_train, y_train):
        
        regressor = BayesianRidge(n_iter = self.n_iter,
                 tol = self.tol,
                 alpha_1 = self.alpha_1,
                 alpha_2 = self.alpha_2,
                 lambda_1 = self.lambda_1,
                 lambda_2 = self.lambda_2,
                 compute_score = self.compute_score,
                 fit_intercept = self.fit_intercept,
                 normalize = self.normalize,
                 copy_X = self.copy_X,
                 verbose = self.verbose).fit(X_train, y_train)
        
        return regressor
    



class RandomForestRegression(object):
    
    
    def __init__(self, n_estimators='warn',
                 criterion='mse',
                 max_depth=None,
                 min_samples_split=2,
                 min_samples_leaf=1,
                 min_weight_fraction_leaf=0.0,
                 max_features='auto',
                 max_leaf_nodes=None,
                 min_impurity_decrease=0.0,
                 min_impurity_split=None,
                 bootstrap=True,
                 oob_score=False,
                 n_jobs=None,
                 random_state=None,
                 verbose=0,
                 warm_start=False):
        
        
        
                 self.n_estimators = n_estimators 
                 self.criterion = criterion
                 self.max_depth = max_depth
                 self.min_samples_split = min_samples_split
                 self.min_samples_leaf = min_samples_leaf
                 self.min_weight_fraction_leaf = min_weight_fraction_leaf
                 self.max_features = max_features
                 self.max_leaf_node = max_leaf_node
                 self.min_impurity_decrease = min_impurity_decrease
                 self.min_impurity_split = min_impurity_split
                 self.bootstrap = bootstrap
                 self.oob_score = oob_score
                 self.n_jobs = n_jobs
                 self.random_state = random_state
                 self.verbose = verbose
                 self.warm_start = warm_start

    
    def fit(self, X_train, y_train):
        
        regressor = RandomForestRegressor(n_estimators = self.n_estimators,
                 criterion = self.criterion,
                 max_depth = self.max_depth,
                 min_samples_split = self.min_samples_split,
                 min_samples_leaf = self.min_samples_leaf,
                 min_weight_fraction_leaf = self.min_weight_fraction_leaf,
                 max_features = self.max_features,
                 max_leaf_node = self.max_leaf_node,
                 min_impurity_decrease = self.min_impurity_decrease,
                 min_impurity_split = self.min_impurity_split,
                 bootstrap = self.bootstrap,
                 oob_score = self.oob_score,
                 n_jobs = self.n_jobs,
                 random_state = self.random_state,
                 verbose = self.verbose,
                 warm_start = self.warm_start).fit(X_train, y_train)
        
        return regressor
    



class RidgeRegression(object):
    
    
    def __init__(self, alpha=1.0,
                 fit_intercept=True,
                 normalize=False,
                 copy_X=True,
                 max_iter=None,
                 tol=0.001,
                 solver='auto',
                 random_state=None):
        
        
        
                 self.alpha = alpha
                 self.fit_intercept = fit_intercept
                 self.normalize = normalize
                 self.copy_X = copy_X
                 self.max_iter = max_iter
                 self.tol = tol
                 self.solver = solver
                 self.random_state = random_state
    
    def fit(self, X_train, y_train):
        
        regressor = Ridge(alpha = self.alpha,
                 fit_intercept = self.fit_intercept,
                 normalize = self.normalize,
                 copy_X = self.copy_X,
                 max_iter = self.max_iter,
                 tol = self.tol,
                 solver = self.solver,
                 random_state = self.random_state).fit(X_train, y_train)
        
        return regressor