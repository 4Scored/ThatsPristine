import pandas as pd
from dateutil import parser

BOOL_VALS_MAP = {
    "true" : True, "false" : False, 
    "t" : True, "f" : False, 
    "1" : True, "0" : False,
    "yes" : True, "no" : False,
}

def convert_types(df, bool_involved=True, inplace=False):
    if not inplace:
        df = df.copy() 

    for col in df.columns:
        if pd.api.types.is_numeric_dtype(df[col]) \
        or pd.api.types.is_datetime64_any_dtype(df[col]) \
        or pd.api.types.is_bool_dtype(df[col]):
            continue
            
        converted = False

        # Numeric Conversion    
        try:
            df[col] = pd.to_numeric(df[col])
            converted = True
        except:
            pass

        # Boolean Conversion
        try:
            if bool_involved and not converted:
                valid_bool_vals = set(BOOL_VALS_MAP.keys())
                
                lowercased_col_bool_vals = df[col].dropna().astype(str).str.strip().str.lower()                                
                if (set(lowercased_col_bool_vals.unique())).issubset(valid_bool_vals):
                    df[col] = lowercased_col_bool_vals.map(BOOL_VALS_MAP).astype(bool)
                    converted = True                    
        except:
            pass

        # Datetime Conversion
        try:
            if not converted:
                parsed = [] 
                for date in df[col]:
                    try:
                        parsed.append(parser.parse(str(date)))
                    except:
                        parsed.append(pd.NaT) 
                parsed = pd.Series(parsed)  
                if parsed.notna().sum() >= 0.2 * len(parsed):
                    df[col] = parsed
                    converted = True
        except:
            pass

    return df 
