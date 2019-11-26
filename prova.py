import pandas as pd
import os

df = pd.read_excel(os.path.join(os.getcwd(), 'data_cripto', 'aion1Dec_15Gen2017_18_data.xlsx'))
print(df.columns)