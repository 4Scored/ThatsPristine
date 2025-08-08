import pandas as pd
from sklearn.impute import KNNImputer

def fill_missing_vals(df, numeric_fill_strat="mean", datetime_fill_strat="mean", inplace=False):
    if not inplace:
        df = df.copy()

    # Filling Numeric Columns
    num_cols = df.select_dtypes(include="number").columns
    for col in num_cols:
        try:
            if numeric_fill_strat == "mean":
                df[col] = df[col].fillna(value=df[col].mean())
            elif numeric_fill_strat == "median":
                df[col] = df[col].fillna(value=df[col].median())
            elif numeric_fill_strat == "mode":
                df[col] = df[col].fillna(value=df[col].mode()[0])
            elif numeric_fill_strat == "knn":                
                non_num_cols = df.drop(num_cols, axis=1)
                knnImputer = KNNImputer(n_neighbors=2)
                df_knnImputed = pd.DataFrame(knnImputer.fit_transform(df[num_cols]), columns=num_cols, index=df.index)                
                df = pd.concat([df_knnImputed, non_num_cols], axis=1)[df.columns] 
            else:
                pass              
        except:
            pass

    # Filling Datetime Columns
    datetime_cols = df.select_dtypes(include="datetime64").columns
    for col in datetime_cols:
        try:
            if datetime_fill_strat == "mean":
                df[col] = df[col].fillna(value=df[col].mean())
            elif datetime_fill_strat == "median":
                df[col] = df[col].fillna(value=df[col].median())
            elif datetime_fill_strat == "mode":
                df[col] = df[col].fillna(value=df[col].mode()[0])
            elif datetime_fill_strat == "forward_backward": 
                df[col] = df[col].ffill()
                df[col] = df[col].bfill()
            elif datetime_fill_strat == "backward_forward": 
                df[col] = df[col].bfill()
                df[col] = df[col].ffill()                
        except:
            pass
    
    return df