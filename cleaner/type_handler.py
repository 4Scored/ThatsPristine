import pandas as pd
from dateutil import parser

def convert_types(df, bool_involved=True):
    df = df.copy()
    for col in df.columns:
        converted = False

        # Numeric Conversion    
        try:
            df[col] = pd.to_numeric(df[col])
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
                if parsed.notna().sum() >= 0.95 * len(parsed):
                    df[col] = parsed
                    converted = True
        except:
            pass

        # Boolean Conversion
        try:
            if bool_involved and not converted:
                bool_like_vals = {"true" : True, "false" : False, 
                                  "t" : True, "f" : False, 
                                  "1" : True, "0" : False,
                                  "yes" : True, "no" : False,
                                  }
                valid_bool_vals = set(bool_like_vals.keys())
                
                lowercased_col_bool_vals = df[col].dropna().astype(str).str.strip().str.lower()                                
                if (set(lowercased_col_bool_vals.unique())).issubset(valid_bool_vals):
                    df[col] = lowercased_col_bool_vals.map(bool_like_vals).astype(bool)
                    converted = True
                    
        except:
            pass

    return df
