import pandas as pd
from sklearn.impute import KNNImputer

def fill_missing_vals(df, fill_strat="mean"):
    df = df.copy()

    # Filling Numeric Columns
    num_cols = df.select_dtypes(include="number").columns
    for col in num_cols:
        try:
            if fill_strat == "mean":
                df[col].fillna(value=df[col].mean(), inplace=True)
            elif fill_strat == "median":
                df[col].fillna(value=df[col].median(), inplace=True)
            elif fill_strat == "mode":
                df[col].fillna(value=df[col].mode()[0], inplace=True)
            elif fill_strat == "knn":                
                non_num_cols = df.drop(num_cols, axis=1)
                knnImputer = KNNImputer(n_neighbors=2)
                df_knnImputed = pd.DataFrame(knnImputer.fit_transform(df[num_cols]), columns=num_cols, index=df.index)                
                df = pd.concat([df_knnImputed, non_num_cols], axis=1)[df.columns] 
            else:
                pass              
        except:
            pass
            
    return df