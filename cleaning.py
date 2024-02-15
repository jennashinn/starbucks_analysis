# %% [markdown]
# ## Part 1 : Data Cleaning and Preparation

# %%
import numpy as np 
import pandas as pd

import warnings
warnings.filterwarnings("ignore")


# %%
df_customer = pd.read_csv('data/profile.csv').drop('Unnamed: 0', axis = 1)
df_offer = pd.read_csv('data/portfolio.csv').drop('Unnamed: 0', axis = 1)
df_transcript = pd.read_csv('data/transcript.csv').drop('Unnamed: 0', axis = 1)

## Customer
# %%
df_customer.head(3)
customer = df_customer.copy()

# %%
# Missing data
missing_percent = round(df_customer.isna().mean() * 100, 1)
pd.DataFrame(missing_percent[missing_percent > 0], columns=["% of Missing Values"])

# %% [markdown]
# All of the missing values come from two columns in df_customer: gender and income. 
# The missing values account for 12.8% of the data in each column. All though it's not ideal, the missing values will be removed.

# %%
customer.dropna(inplace = True)
customer.info()


# became_member_on looks like it should be a date, not an integer:
customer['became_member_on'] = pd.to_datetime(customer['became_member_on'], format = '%Y%m%d')

# Knowing that it will probably be helpful during EDA, I'm going to go ahead and add a few day, month, and year columns.
customer['year'] = customer['became_member_on'].dt.year
customer['month_number'] = customer['became_member_on'].dt.month
customer['day_of_month'] = customer['became_member_on'].dt.day
customer['month'] = customer['became_member_on'].dt.month_name()
customer['day_number'] = customer['became_member_on'].dt.weekday
customer['day'] = customer['became_member_on'].dt.day_name()

customer.head()


# %% [markdown]
# Offer 

# %%
df_offer.head(3)

# %%
# No missing data
df_offer.isna().sum()

# %%
df_offer.info()

# %%
# Looking at the different offer_types
df_offer['offer_type'].unique()

# %%
# Looking at the different channels
df_offer['channels'].unique()
# Offer is clean

# %% [markdown]
# Transcript

# %%
df_transcript.head(3)
transcript = df_transcript.copy()

# %%
print(df_transcript['value'])

# %%
## Cleaning up the 'value' column

# Splitting the values based on ":"
split_values = transcript['value'].str.split(':', n=1, expand=True)

# Renaming the columns
split_values.columns = ['key', 'value']

# Remove curly braces and single quotes from the 'key' and 'value' columns using lambda function
split_values['key_id'] = split_values['key'].apply(lambda x: x.replace('{', '').replace('}', '').replace("'", '').strip())
split_values['value_id'] = split_values['value'].apply(lambda x: x.replace('{', '').replace('}', '').replace("'", '').strip())

# Concatenating the split values DataFrame with the original DataFrame
transcript_ = pd.concat([transcript, split_values], axis=1)
transcript_.head()

# # %%
cleaned_transcript = transcript_.drop(['value', 'key'], axis = 1)
# %%
# Change time to hours_since_start
cleaned_transcript = cleaned_transcript.rename(columns = {'time' : 'hours_since_start'})





### Save the datasets that were cleaned for part 2
customer.to_csv('data/cleaned_customer.csv', index = False)
cleaned_transcript.to_csv('data/cleaned_transcript.csv', index= False)