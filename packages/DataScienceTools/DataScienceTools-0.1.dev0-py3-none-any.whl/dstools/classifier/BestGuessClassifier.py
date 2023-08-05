import pandas as pd
import numpy as np
from sklearn.base import BaseEstimator
from sklearn.metrics import mean_absolute_error


class BestGuessClassifier(BaseEstimator):
    
    
    """
    The BestGuessClassifier creates a constant numeric best guess for a given metric, e.g. mean absolute squared error. This Classifier is for interval scaled numeric dependent variables. Use this classifier for binnend variables, otherwise use dstools.regressors.BestGuessRegressor.
    
    Parameters
    ----------
    
    metric: function(y_true, y_predicted), default=sklearn.metrics.mean_absolute_error
        The best guess ist optmized on the given metric, either minimum or maximum.
        
    argmin: bool, default=True
        The given metric is either optimized on argmin or argmax. Argmin for True and argmax for False.


    Functions
    ---------

        __str__
            returns the name of the classifier as string

        fit(X, y)
            fit the classifier on the argmin or argmax of a given metric (default=sklearn.metrics.mean_absolute_error)

        predict(X, y=None)
            returns an pandas.Series with the constant best guess
      
        
    Examples
    --------
    
    The BestGuessClassifier is insensitive to X values
    >>>y=[1,2,3]
    >>>y_pred = BestGuessClassifier().predict(X)
    >>>y_pred
    [2,2,2]

    """
    
    def __init__(self, metric=mean_absolute_error, argmin=True):
        
        self.best_guess_ = 42 #the answer to everyhing
        self.metric = metric
        self.argmin = argmin
  
        
    def __str__(self):
        
        return 'BestGuessClassifier'
    
        
    def fit(self, X, y):

        """
        fit the dstools.classifier.BestGuessClassifier by using the argmin or argmax of a given metric (default=sklearn.metrics.mean_absolute_error)

        Parameters
        ----------

            X: pandas.DataFrame
                independent variables

            y: pandas.Series, default=None
                dependent variable


        Output
        ------

            None

        """
        
        # create range of all possible classes
        classes = np.unique(y)
        
        # get either argmin or argmax of a metric score to optimize the best guess
        #argmin, argmax return the index of the best class
        if self.argmin:
            
            self.best_guess_ = classes[np.argmin([self.metric(y,np.full(len(y),x)) for x in classes])]
        
        else:
            
            self.best_guess_ = classes[np.argmax([self.metric(y,np.full(len(y),x)) for x in classes])]
               
    
    def predict(self, X, y=None):

        """
        returns a constant best guess following the given metric (default=sklearn.metrics.mean_absolute_error)

        Parameters
        ----------

            X: pandas.DataFrame
                independent variables

            y: pandas.Series, default=None
                dependent variable, not needed in predict


        Output
        ------

            pandas.Series containing a constant best guess for the dependent variable

        """
        
        #create a return a Series with the best guess
        y_predicted = pd.Series(np.full(X.shape[0], self.best_guess_))
        return y_predicted
