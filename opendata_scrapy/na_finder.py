import os
import pandas as pd
import glob
import numpy as np
count = 0
length = 0
path = "/Users/ireneroma/Documents/8WIRES/Productes/OpenData Report/opendata_report/VAL_csv/*.csv"
for fname in glob.glob(path):
    df = pd.read_csv(fname, na_values='', keep_default_na=False, error_bad_lines=False)
    if len(df)==0:
        pass
    else:
        count += np.mean(df.isnull().sum()/len(df)*100)
        length += 1
        print fname
        print count
print length
print count
print count/length
