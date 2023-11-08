import sqlite3
import pandas as pd

# load the data
df = pd.read_csv('datafiles/Continent_Consumption_TWH.csv')
# clean the data
# df.columns = df.columns.strip()
# create the connection
conn = sqlite3.connect('db.sqlite3')
# write the data to a sqlite3 table.
df.to_sql('statistics_continentconsumption', conn, if_exists='replace',
          index=False)
# close the connection
conn.close()
