import pandas as pd
from sqlalchemy import create_engine
# accounts database
accounts_data = {
    'username': ['poop'],
    'password': ['peep']
}

accounts_df = pd.DataFrame(accounts_data)
accounts_df.to_sql('accounts', con=create_engine('sqlite:///final_project/static/accounts.db'), if_exists='replace', index=False)

# journal entries database
entries_data = {
    'username': [],
    'title': [],
    'entry': [],
    'datestamp': []
}

entries_df = pd.DataFrame(entries_data)
entries_df.to_sql('entries', con=create_engine('sqlite:///final_project/static/entries.db'), if_exists = 'replace', index=False)