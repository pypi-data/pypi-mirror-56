import pandas as pd 
import numpy as np
from sklearn.base import TransformerMixin

class OneHotEncoder(TransformerMixin):

    """
    This module performs binary encoding on columns containing categorical data.
    It assumes that all non numeric columns contain categorical data. If categorical data is encoded in numeric columns, use dstools.preprocessing.FeatureConverter to convert these values first. The maximum number of encoded values can be given globally or fine tuned for every column. Values that exceed the maximum number of encoded values are aggregated in a REST class. Missing values can be either put in the REST class or be classified as distinct value. Categrocial columns with exactly two values (including missing values) can be encoded into one column to reduce dimensionality.

    Parameters
    ----------

        number_of_top_values: int, default=10
            maximum number of distinct values of each column to be encoded, lower priority than special_columns

        special_columns: dict, default={}
            mmaximum number of distinct values to be encoded in certain columns, higher priority than number_of_top_values, form {column:number_of_top_values}

        dropna: boolean, default=False
            if True missing values are not recognized as distinct values and will be put in REST class, if False missing values will be recognized as distinct values

        compress_binary; boolean, default=False
            if True columns with exactly two distinct values will be encoded into a single binary column. ATTENTION: dropna will be ignored, missing values are counted as distinct value


    Output
    ------
    
        pd.DataFrame with encoded values
        
        
    Functions
    ---------
    
        fit(X, y=None):
            indentify columns and values to be encoded
            
        transform(X, y=None)
            perform binary encoding on categorical data
            
        fit_transform(X, y=None)
            performs fit and transform
            
    
    Examples
    --------

        1 categorical column
        >>>df = pd.DataFrame({'x':['a','b','c']})
        >>>OneHotEncoder().fit_transform(df)
        x_OHE_a x_OHE_b x_OHE_c
        1   0   0
        0   1   0
        0   0   1


        number of top values exceeded
        >>>df = pd.DataFrame({'x':['a','a','c']})
        >>>OneHotEncoder(number_of_top_values=1).fit_transform(df)
        x_OHE_a x_OHE_REST
        1   0   
        1   0   
        0   1           


        special columns
        >>>df = pd.DataFrame({'x':['a','a','c']})
        >>>OneHotEncoder(number_of_top_values=1, special_columns={'x':2}).fit_transform(df)
        x_OHE_a x_OHE_c
        1   0   
        1   0   
        0   1    


        missing values
        >>>df = pd.DataFrame({'x':['a','a',np.NaN]})
        >>>OneHotEncoder(number_of_top_values=2, dropna=False).fit_transform(df)
        x_OHE_a x_OHE_nan
        1   0   
        1   0   
        0   1   
        >>>df = pd.DataFrame({'x':['a','a',np.NaN]})
        >>>OneHotEncoder(number_of_top_values=2, dropna=True).fit_transform(df)
        x_OHE_a x_OHE_REST
        1   0   
        1   0   
        0   1  


        binary compression 
        >>>df = pd.DataFrame({'x':['a','a','c']})
        >>>OneHotEncoder(number_of_top_values=2, compress_binary=True).fit_transform(df)
        x_a/c
        1      
        1      
        0   
            
    """


    def __init__(self, number_of_top_values = 10, special_columns = {}, dropna=False, compress_binary=False):

        self.number_of_top_values = number_of_top_values
        self.top_values = {}
        self.special_columns = special_columns
        self.columns_to_encode = []
        #self.columns_to_keep = []
        self.dropna = dropna
        self.compress_binary = compress_binary


    def fit(self, X, y=None):

        """
        Parameters
        ----------
        
            X: pd.DataFrame
                features to be encoded
                
            y: pd.Series
                will not be used, just necessary for sklearn syntax
                
        Output
        ------
        
            None
        """

        #only non numeric columns get encoded
        numerics = [np.int8, np.int16, np.int32, np.int64, np.float32, np.float64]
        self.columns_to_encode = X.select_dtypes(exclude=numerics).columns

        #create a dicitonary with all values of a column to be encoded, key is the column
        for column in self.columns_to_encode:

            #number of values to be encoded is specified in special_columns
            if column in self.special_columns:
                self.top_values[column] = X[column].value_counts(dropna=self.dropna).sort_values(ascending=False).index[0:self.special_columns[column]]

            #number of values to be encoded is given by number_of_top_values
            else:
                self.top_values[column] = X[column].value_counts(dropna=self.dropna).sort_values(ascending=False).index[0:self.number_of_top_values]


    def transform(self, X, y=None):

        """
        Parameters
        ----------
        
            X: pd.DataFrame
                features to be encoded
                
            y: pd.Series
                will not be used, just necessary for sklearn syntax
                
        Output
        ------
        
            pandas.DataFrame with encoded features
        """

        X_transformed = X.copy()
       
        #encode values for every columns with categorical data       
        for column in self.columns_to_encode:

            #columns with only two values (including missing) can be compressed into one binary encoded column
            if self.compress_binary and X_transformed[column].value_counts(dropna=False).shape[0]==2 and len(self.top_values[column]==2):

                value1 = self.top_values[column][0]
                value2 = self.top_values[column][1]

                X_transformed[column+'_'+str(value1)+'/'+str(value2)] = X_transformed[column].apply(lambda x: 1 if str(x) == str(value1) else 0)

            #one column for every encoded value
            else:

                #create a new binary encoded column for every value to be encoded
                for value in self.top_values[column]:

                    #string equality is necessary to handle missing values
                    X_transformed[column+'_OHE_'+str(value)] = X_transformed[column].apply(lambda x: 1 if str(x) == str(value) else 0)

                #if there are more different values than values to be encoded, initialize a REST class
                if X_transformed[column].value_counts(dropna=False).shape[0] > len(self.top_values[column]):

                    X_transformed[column+'_OHE_REST'] = X_transformed[column].apply(lambda x: 1 if x not in self.top_values[column] else 0)

        #drop the original columns
        X_transformed.drop(self.columns_to_encode, axis=1, inplace=True)
        
        return X_transformed


    def fit_transform(self, X, y=None):

        """
        execute fit & transform

        Parameters
        ----------
        
            X: pd.DataFrame
                features to be encoded
                
            y: pd.Series
                will not be used, just necessary for sklearn syntax
                
        Output
        ------
        
            pandas.DataFrame with encoded features
        """

        self.fit(X)
        X = self.transform(X)

        return X

        
