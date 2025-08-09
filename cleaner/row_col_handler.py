import warnings
import pandas as pd

def handle_outliers(df, cols_criteria, handle_strat="iqr", inplace=False):
    if not inplace:
        df = df.copy()

    if isinstance(cols_criteria, str):
        cols_criteria = [cols_criteria]

    existing_cols = [col for col in cols_criteria if col in df.columns]
    missing_cols = set(cols_criteria) - set(existing_cols)          
    if missing_cols:
        warnings.warn(f"Criteria Column(s) {missing_cols} DNE")     

    num_cols = list(set(existing_cols) & set(df.select_dtypes(include="number").columns))
    non_num_cols = set(existing_cols) - set(num_cols)
    if non_num_cols:
        warnings.warn(f"Non-Numeric Column(s) {non_num_cols} Skipped Over")

    if not num_cols:
        return df

    mask_all = pd.Series(True, index=df.index)

    for col in num_cols:
        x = df[col]
        if handle_strat == "iqr":
            q1, q3 = x.quantile(0.25), x.quantile(0.75)
            iqr = q3 - q1
            if pd.isna(iqr) or iqr == 0:
                col_mask = pd.Series(True, index=df.index, dtype=bool) # "Do Nothing" Mask
            else:
                lower_fence, upper_fence = q1 - 1.5*iqr, q3 + 1.5*iqr            
                col_mask = ((x >= lower_fence) & (x <= upper_fence)) | x.isna()
        elif handle_strat == "z_score":  
            col_mean, col_std = x.mean(), x.std()
            if pd.isna(col_std) or col_std == 0:
                col_mask = pd.Series(True, index=df.index, dtype=bool)
            else:
                z_scores = (x - col_mean) / col_std
                col_mask = ((z_scores >= -3) & (z_scores <= 3)) | x.isna()
        elif handle_strat == "quantile":
            q1, q3 = x.quantile(0.05), x.quantile(0.95)
            iqr = q3 - q1
            if pd.isna(iqr) or iqr == 0:
                col_mask = pd.Series(True, index=df.index, dtype=bool)
            else:
                lower_fence, upper_fence = q1 - 1.5*iqr, q3 + 1.5*iqr
                col_mask = ((x >= lower_fence) & (x <= upper_fence)) | x.isna()
        else:
            warnings.warn(f"{handle_strat}: Unknown Outlier Handing Strategy")
            col_mask = pd.Series(True, index=df.index, dtype=bool)
        
        mask_all &= col_mask

    df = df[mask_all]
    return df

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