import warnings

def drop_columns(df, cols_to_drop):
    df = df.copy()
    existing_cols = [col for col in cols_to_drop if col in df.columns]
    missing_cols = set(cols_to_drop) - set(existing_cols)          
    if missing_cols:
        warnings.warn(f"Column(s) {missing_cols} DNE") 
    df.drop(columns=existing_cols, inplace=True)
    return df

def drop_duplicates(df):        
    return df.drop_duplicates()