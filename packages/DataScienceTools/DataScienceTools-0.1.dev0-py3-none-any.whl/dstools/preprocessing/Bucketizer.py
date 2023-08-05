import numpy as np
import pandas as pd
from sklearn.base import TransformerMixin


class Bucketizer(TransformerMixin):

    """
    The Bucketizer puts numeric features into bins. The binned feature can either replace the original feature or can be created additionally. You can bin all numeric features, pass a list of the features to be binned or pass prefix of the features to be binned.

    Parameters
    ----------

        bins: int, default=2
            Number of bins to be created.

        replace: boolean, default=True
            If True the original feature will be replaced by the binned feature. If False the binned feature will be created next to the original feature.

        features: list, default=[]
            List of column names. Columns contain the features to be put into binned.

        prefix: string, default=None
            Prefix of features to be binned.

        bin_numeric: boolean, default=True
            If True, binning will be performed on all numeric columns. If False, only the columns in features or with a passed prefix will be binned.

    
    Output
    ------

        pandas.DataFrame with the binned features


    Attributes
    ----------

        self.numerics: list, default=['int16', 'int32', 'int64', 'float16', 'float32', 'float64']
            Data types to be considered numeric, necessary for fitting and transforming only numeric values.

        self.quantiles: dict, default={}
            Dictionary of feature columns (=key) and quantiles according to number of bins (=values).


    Functions
    ---------

        fit(X, y=None):
            Fit the Bucketizer by creating a dictionary with Feature columns as key and quantiles as values.
            
        transform(X, y=None)
            Create the binned feature columns.
            
        fit_transform(X, y=None)
            Performs fit and transform.

        calculate_feature_bin(x, quantile_list)
            Assign bin to feature values according to quantiles.


    Examples
    --------

        bin one numeric feature
        >>>df=pandas.DataFrame({'x':[1,2,3]})
        >>>Bucketizer(bins=1, bin_numeric=True).fit_transform(df)
        'x'
        0
        0
        0

        multiple bins
        >>>df=pandas.DataFrame({'x':[1,2,3,4]})
        >>>Bucketizer(bins=2, bin_numeric=True).fit_transform(df)
        'x'
        0
        0
        1
        1

        keep original column
        >>>df=pandas.DataFrame({'x':[1,2,3]})
        >>>Bucketizer(bins=1, bin_numeric=True, replace=False).fit_transform(df)
        'x' 'x_binned'
        1   0
        2   0
        3   0

    """


    def __init__(self, bins=2, replace=True, features=[], prefix=None, bin_numeric=False):
        
        self.bins = bins
        self.features = features.copy() #in case multiple objects are initiated
        self.prefix = prefix
        self.replace = replace
        self.quantiles = {}
        self.bin_numeric = bin_numeric
        self.numerics = ['int16', 'int32', 'int64', 'float16', 'float32', 'float64']


    def fit(self, X, y=None):

        """
        fits the Bucektizer
        
        Parameters
        ----------
        
            X: pd.DataFrame
                DataFrame with the features to be binned
                
            y: pd.Series
                will not be used, just necessary for sklearn syntax
                
        """

        #bin all numeric features
        for column in X.columns:

            #bin all numeric features, if not already passed in feature list
            if self.bin_numeric and column not in self.features and X[column].dtype in self.numerics:

                self.features.append(column)

            #bin numeric features with prefix, if not passed in feature list, prefix must be passed
            if self.prefix:
                
                if self.prefix in column and column not in self.features and X[column].dtype in self.numerics:

                    self.features.append(column)

        #create a dictionary with features as keys and quantiles as values
        for feature in self.features:

            #features must be numeric
            if X[feature].dtype in self.numerics:

                #init a list with 0 percent quantile als starting value
                quantile_list = [0]

                #find a quantile for every bin
                for i in range(self.bins):

                    #add fraction according to number of bins to largest quantile
                    quantile_list.append(quantile_list[-1] + 1.0 / self.bins)
                    #print(q_f_list)

                #add quantiles to dictionary
                self.quantiles[feature] = [np.quantile(X[feature], f) for f in quantile_list]

            else:

                print(f"Caution: non numeric feature {feature} passed, no binning performed")


    def transform(self, X, y=None):

        """
        bins values and returns the transformed DataFrame
        
        Parameters
        ----------
        
            X: pd.DataFrame
                DataFrame with the features to be binned
                
            y: pd.Series
                will not be used, just necessary for sklearn syntax
             
        """

        X_transformed = X.copy()

        for feature in self.features:

            if X[feature].dtype in self.numerics:
                
                if self.replace:

                    name = feature

                else:

                    name = feature + '_binned'

                #assign a bin, depending on value
                X_transformed.loc[:, name] = X_transformed[feature].apply(lambda x: self.calculate_feature_bin(x, self.quantiles[feature]))

            else:

                print(f"Caution: non numeric feature {feature} passed, no binning performed")

        return X_transformed


    def fit_transform(self, X, y=None):

        """
        Parameters
        ----------
        
            X: pd.DataFrame
                features to be converted
                
            y: pd.Series
                will not be used, just necessary for sklearn syntax
                
        Output
        ------
        
            pd.DataFrame with converted featuresfit and transform
        """
        
        self.fit(X)
        return self.transform(X)


    def calculate_feature_bin(self, x, quantile_list):

        """
        match values to bins according to fitted quantiles

        Parameters
        ----------

            x: int
                value to be matched with quantlies to be put in a bin

            quantile_list: list
                list of all quantiles defining bin borders

        Output
        ------

            int
                index for bin
                
        """

        i = 0 #not sure, if necessary

        #qunatile list has 0 percent quantile, ignore that
        for i in range(len(quantile_list) - 1):

            #if value is between quantile (in a percentile)
            if quantile_list[i] <= x < quantile_list[i+1] + 0.0000001:

                return i

        return i
