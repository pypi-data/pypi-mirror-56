import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.base import TransformerMixin

class NumScaler(TransformerMixin):
  
    """
    NumScaler is a wrapper for scalers. Some scalers only take numerical input and can't ignore non numerical data. NumScaler identifies numerical data and passes it to a Scaler (default=sklearn.preprocessing.StandardScaler).

    Parameters
    ----------

        scaler: scaler object, default=sklearn.preprocessing.StandardScaler()
            scaler object with sklearn conform fit and transform functions


    Output
    ------

        pandas.DataFrame with scaled numerical data and non scaled non numerical data


    Functions
    ---------

        fit(X, y=None)
            identifies numerical columns, passes it forward and fits the scaler

        transform(X, y=None)
            performs the transform function of the scaler on the numerical data and returns the transformed data with scaled numerical and non scaled non numerical values

        fit_transform(X, y=None)
            performs fit & transform

    
    Examples
    --------

        >>>df = pandas.DataFrame({'x1':[1,2,3,4],'x2':['a','b','c','d']})
        >>>NumScaler().fit_transform(df)
            x1 x2
        0 -1.341641  a
        1 -0.447214  b
        2  0.447214  c
        3  1.341641  d

    """
  
    def __init__(self, scaler=StandardScaler()):

        self.numeric_columns = []
        self.scaler = scaler
    
    
    def fit(self, X, y=None):
  
        """
        identifies numeric columns and fits the scaler

        Parameters
        ----------

            X: pandas.DataFrame
                pandas.DataFrame containing the features to be processed

            y: pandas.Series, default=None
                just for sklearn conformity


        Output
        ------

            None

        """

        #identify numerical values
        numerics = ['int16', 'int32', 'int64', 'float16', 'float32', 'float64']
        self.numeric_columns = X.select_dtypes(include=numerics).columns
    
        #if there are numerical values, fit the scaler with them
        if len(self.numeric_columns)>0: 
            self.scaler.fit(X[self.numeric_columns], y)
    
    
    def transform(self, X, y=None):

        """
        scales numeric values

        Parameters
        ----------

            X: pandas.DataFrame
                pandas.DataFrame containing the features to be processed

            y: pandas.Series, default=None
                just for sklearn conformity


        Output
        ------

            pandas.DataFrame with the processed features

        """        
        
        X_transformed = X.copy()

        #if numeric values exist, scale them
        if len(self.numeric_columns)>0:
            X_transformed.loc[:,self.numeric_columns] = self.scaler.transform(X[self.numeric_columns])

        return X_transformed


    def fit_transform(self, X, y=None):

        """
        identifies numeric columns, fits the scaler and scales numerical values

        Parameters
        ----------

            X: pandas.DataFrame
                pandas.DataFrame containing the features to be processed

            y: pandas.Series, default=None
                just for sklearn conformity


        Output
        ------

            pandas.DataFrame with the processed features

        """           

        self.fit(X, y)
        return self.transform(X, y)
