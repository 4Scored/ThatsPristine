import string

def clean_text(df, normalize=False, remove_punc=False):
    df = df.copy()
    obj_cols = df.select_dtypes(include="object")
    for col in obj_cols:
        df[col] = df[col].astype(str).str.strip()
        if normalize:
            df[col] = df[col].astype(str).str.lower()
        if remove_punc:
            print("CHECK")
            df[col] = df[col].astype(str).str.translate(str.maketrans('', '', string.punctuation))   
            print(df[col])
            print("CHECK")
    return df