import pandas as pd
import sqlite3 as lite
import plotly.express as px


#conecting sql db
sqliteConnection = lite.connect('CryptoPunk.db')
cursor = sqliteConnection.cursor()

# Question 2
#query to report the punk with the highest price

query_max_price = """SELECT PunkID, MAX(TAmt) Max_Price
                FROM PunkTrades
                WHERE TType == 'Sold'
                ORDER By Max_Price DESC
                LIMIT 1
                """

query_max_price_df = pd.read_sql_query(query_max_price,sqliteConnection)
print(query_max_price_df.head())

# Question 3
# Punk which was traded the most

query_most_traded = """SELECT PunkID, count(*) as Num_Trades
                FROM PunkTrades
                GROUP BY PunkID
                ORDER BY Num_Trades DESC
                LIMIT 1"""

query_most_traded_df = pd.read_sql_query(query_most_traded,sqliteConnection)
print(query_most_traded_df.head())      


# Question 4
#query to report average price per date
query_avg_price = """SELECT TDate, AVG(TAmt) Avg_Price 
                FROM PunkTrades
                WHERE TType == 'Sold'
                GROUP BY TDate
                ORDER BY TDate ASC
                """

query_avg_price_df = pd.read_sql_query(query_avg_price,sqliteConnection)
print(query_avg_price_df.head())
fig_avg_price = px.histogram(query_avg_price_df, x="TDate", y="Avg_Price", labels={"TDate" : "Date", "Avg_Price" : "Average Price"}, title="Average price per date")
fig_avg_price.show()

# Question 5
# Owner with Most Valuable Portfolio

query_val_portfolio = """ SELECT TTo, SUM(TAmt) as total_amount
                        FROM PunkTrades
                        WHERE TType = 'Sold'
                        GROUP BY TTo
                        ORDER BY total_amount DESC
                        LIMIT 25
                        """
query_val_portfolio_df = pd.read_sql_query(query_val_portfolio,sqliteConnection)
print(query_val_portfolio_df.head())
fig_val_port = px.scatter(query_val_portfolio_df, x="total_amount", y="total_amount",
	         size="total_amount", color="TTo",
                log_x = True, size_max=30, title="Most Valuable Portfolio")
fig_val_port.show()