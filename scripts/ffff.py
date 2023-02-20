import pandas as pd

df = pd.read_csv('linkedin_url.csv')
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
print(df.dropna())