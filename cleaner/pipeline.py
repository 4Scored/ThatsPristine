import pandas as pd
from cleaner.type_handler import convert_types
from cleaner.impute_handler import fill_missing_vals
from cleaner.row_col_handler import drop_duplicates, drop_columns, handle_outliers
from cleaner.text_handler import clean_text_data, clean_column_names

def run_basic_pipeline(df):    
    df = convert_types(df, True)
    df = fill_missing_vals(df, numeric_fill_strat="knn", datetime_fill_strat="mean")
    df = drop_duplicates(df)
    df = clean_text_data(df, normalize=True)
    df = clean_column_names(df, normalize=True)
    return df