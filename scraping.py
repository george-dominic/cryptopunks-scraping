import requests
from bs4 import BeautifulSoup
import random
import pandas as pd
import time
import datetime as dt
import sqlite3 as lite

BaseStr = "https://www.larvalabs.com/cryptopunks/details/"
class_no = 1
count = 1000+(class_no*100)
con = lite.connect('CryptoPunk.db')

with con:
    cur=con.cursor()
    cur.execute("DROP TABLE IF EXISTS PunkTrades")
    cur.execute("""CREATE TABLE PunkTrades(TDate INT, PunkID INT,
    TType TEXT, TFrom TEXT, TTo TEXT, TAmt INT)""")
    # Loop over the punk numbers from 1 to 1500
    for punk_number in range(count):

        punk = str(punk_number)
        print("Processing punk number :",punk)
        time.sleep(2 + 0.5 * random.random())
        page = requests.get(BaseStr+punk)
        soup = BeautifulSoup(page.content, "html.parser")
        trade_table = soup.find('table', attrs={'class':'table'})

        # If the trade data table is found, extract the rows and write them to a CSV file
        if trade_table:
            # Extract the table rows
            rows = trade_table.find_all("tr")

            col_order = [4,0,1,2,3]
            # data_df = pd.DataFrame(columns = ['Date', 'Type','From','To','Amount'])
            for row in rows:
                cols = row.find_all('td')

                if not cols:
                    continue

                cols = [ele.text.strip() for ele in cols]
                cols = [cols[i] for i in col_order]
                cols.insert(1,punk)
                cols[0] = dt.datetime.strptime(cols[0], '%b %d, %Y').strftime('%Y-%m-%d')
                cols[-1] = cols[-1].split("Ξ")[0].replace('<',"")
                

                try:
                    cur.execute('''INSERT OR IGNORE INTO PunkTrades(TDate, PunkID, TType, TFrom, TTo, TAmt) VALUES(?,?,?,?,?,?)''',cols)
                except:
                    print("Insertion error: row wasn't inserted", cols)
