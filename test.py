import pandas as pd

df_url = pd.read_csv('list.csv', header=None, names=['url'])
count = 0
for index, row in df_url.iterrows():
    url = row['url']
    print("http://api.scraperapi.com?api_key=9bcf40e14bb4e30ded56421f15645949&url="+ url)