"""import pandas as pd

# Empty list
df = pd.DataFrame(columns=['full_name', 'current_title', 'location', 'summary', 'skills', 'education', 'experience',
                           'certifications', 'languages', 'url'])

# It will make Empty Pickle File in same folder in which code is running
pd.to_pickle(df, "data/scraped_profiles.pkl")
"""
import pickle as pkl
import pandas as pd
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
pd.options.display.max_colwidth = 1000
"""with open("data/scraped_profiles.pkl", "rb") as f:
    object = pkl.load(f)

df = pd.DataFrame(object)
df.to_csv(r'file.csv')"""

a = pd.read_csv('file.csv', header=None)

print(a)