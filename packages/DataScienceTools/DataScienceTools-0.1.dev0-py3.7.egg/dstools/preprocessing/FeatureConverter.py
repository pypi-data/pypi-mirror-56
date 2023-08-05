from sklearn.base import TransformerMixin
import numpy as np
import pandas as pd

class FeatureConverter(TransformerMixin):
    
    """
    The FeatureConverter helps to integrate common preprocessing steps into sklearn pipelines. Supported preprocessing steps are replacing values, converting to str, int or float, dropping columns or adding flags. Steps will be performed in the following order: create flags, replace values, convert types, drop columns
    
    Parameters
    ----------
    
        columns_to_string: list, default=[]
            list of columns to be converted into string format
            
        columns_to_int: list, default=[]
            list of columns to be converted into int format
            
        columns_to_float: list, default=[]
            list of columns to be converted into int format
            
        columns_with_replace: dictionary of dictionaries, default={}
            dictionary of form {column:{value1:replacement1,value2:replacement2,...},...}
        
        value_flags: dictionary, default={}
            dictionary of form {column:[value]}, column and list of values to be used to create new columns containing a binary flag
            
        columns_to_drop, default=[]
            list of columns to be dropped 
            
            
    Output
    ------
    
        pd.DataFrame with converted values
        
        
    Functions
    ---------
    
        fit(X, y=None):
            do nothing - just for sklearn pipeline syntax
            
        transform(X, y=None)
            performs conversion
            
        fit_transform(X, y=None)
            performs fit and transform
            
    
    Examples
    --------
    
        type conversion
        >>>df_test=pd.DataFrame({'string1':['1','2','3','4'],'string2':['1','2','3','4'],'int':[1,2,3,4]})
        >>>fc=FeatureConverter(columns_to_string='int',columns_to_int='string1',columns_to_float='string2')
        >>>fc.fit_transform(df_test).dtypes
        string1      int64
        string2    float64
        int         object
        dtype: object    
        
        replacement
        >>>df_test=pd.DataFrame({'string1':['1','2','3','4'],'string2':['1','2','3','4'],'int':[1,2,3,4]})
        >>>fc=FeatureConverter(columns_with_replace={'string1':{'1':'hello'},'string2':{'1':'hello','2':'world'},'int':{1:42}})
        >>>fc.fit_transform(df_test)
        	string1	string2	int
        0	hello	hello	42
        1	2	world	2
        2	3	3	3
        3	4	4	4
        
        create flags for values
        >>>df_test=pd.DataFrame({'string1':['1','2','3','4'],'string2':['1','2','3','4'],'int':[1,2,3,4]})
        >>>fc=FeatureConverter(value_flags={'string1':['1'],'string2':['1','2'],'int':[0]})
        >>>fc.fit_transform(df_test)
        	string1	string2	int	string1_1	string2_1	string2_2	int_0
        0	1	1	1	1	1	0	0
        1	2	2	2	0	0	1	0
        2	3	3	3	0	0	0	0
        3	4	4	4	0	0	0	0
        
        drop columns
        >>>df_test=pd.DataFrame({'string1':['1','2','3','4'],'string2':['1','2','3','4'],'int':[1,2,3,4]})
        >>>fc=FeatureConverter(columns_to_drop=['string1'])
        >>>fc.fit_transform(df_test)
        	string2	int
        0	1	1
        1	2	2
        2	3	3
        3	4	4
        
    """
    
    
    def __init__(self, columns_to_string=[], columns_to_int=[], columns_to_float=[], columns_with_replace={}, value_flags={}, columns_to_drop=[]):
        
        self.columns_to_string=columns_to_string
        self.columns_to_int=columns_to_int
        self.columns_to_float=columns_to_float
        self.columns_with_replace=columns_with_replace
        self.value_flags=value_flags
        self.columns_to_drop=columns_to_drop
        
    
    def fit(self, X=None, y=None):
        
        """
        do nothing
        """
        
        pass
        
        
    def transform(self, X, y=None):
        
        """
        Parameters
        ----------
        
            X: pd.DataFrame
                features to be converted
                
            y: pd.Series
                will not be used, just necessary for sklearn syntax
                
        Output
        ------
        
            pd.DataFrame with converted features
                
        """
        
        X_transformed = X.copy()
        
        for column in X_transformed.columns:
            
            #create flags for all passed values
            if column in self.value_flags.keys():
                
                for value in self.value_flags[column]:
                    
                    X_transformed[column+'_'+str(value)] = X_transformed[column].apply(lambda x: 1 if x==value else 0)
            
            #replace values
            if column in self.columns_with_replace:
                
                X_transformed.loc[:,column] = X_transformed[column].replace(self.columns_with_replace[column].keys(),self.columns_with_replace[column].values())
            
            #convert to string
            if column in self.columns_to_string:
                
                X_transformed.loc[:,column] = X_transformed[column].astype(str)
            
            #convert to int
            if column in self.columns_to_int:

                # float values need to be rounded first
                if X_transformed[column].dtype in ['float16', 'float32', 'float64']:

                    X_transformed.loc[:,column] = X_transformed[column].apply(lambda x: round(x))
                
                X_transformed.loc[:,column] = X_transformed[column].astype(int)
            
            #convert to float
            if column in self.columns_to_float:
                
                X_transformed.loc[:,column] = X_transformed[column].astype(float)
            
            #drop column
            if column in self.columns_to_drop:
                
                X_transformed.drop(column, axis=1, inplace=True)
                     
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
        
            pd.DataFrame with converted features
                
        """
    
        self.fit(X, y)
        return self.transform(X, y)
