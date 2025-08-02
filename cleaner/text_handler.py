import string

def clean_text_data(df, normalize=False, remove_punc=False):
    df = df.copy()
    obj_cols = df.select_dtypes(include="object")
    for col in obj_cols:
        df[col] = df[col].astype(str).str.strip()
        if remove_punc: 
            df[col] = df[col].astype(str).str.translate(str.maketrans('', '', string.punctuation)) 
        if normalize: 
            df[col] = df[col].astype(str).str.lower().str.replace(r'\s+', ' ', regex=True)        
    return df

def clean_column_names(df, normalize=False, remove_punc=False):
    df = df.copy()    
    df.columns = df.columns.str.strip()     
    if remove_punc: 
        df.columns = df.columns.astype(str).str.translate(str.maketrans('', '', string.punctuation)) 
    if normalize: 
        df.columns = df.columns.astype(str).str.lower().str.replace(r'\s+', '_', regex=True)  
    return df