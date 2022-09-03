import pandas as pd
from sqlalchemy import create_engine

data=[]
engine=create_engine('sqlite:///weekStock.db',echo=True)

with open("ticker_symbols.txt", "r") as f:
        tickers= [(line.strip()).split() for line in f]
#print(tickers)

#Creating a dictionary to store information from the CSV files we created earlier
for ticker in tickers:
    with open('data/'+str(ticker[0])+'.csv','r') as file:
        info = file.readlines()
    for i in range(1,len(info)):
        row = info[i] 
        row = str(info[i]).split(",") 
        print(row)
        to_convert_to_date_format=row[1]
        row[1]=to_convert_to_date_format[8:10]+'/'+to_convert_to_date_format[5:7]+'/'+to_convert_to_date_format[0:4]
        print(row[1])
        row[8]=row[8].strip('\n')
        my_dict={"id":row[8],"date":row[1],"ticker":row[6],
            "high":round(float(row[3]),2),"low":round(float(row[4]),2),"high_diff":float(row[7])}
        data.append(my_dict)

df=pd.DataFrame(data).set_index('id')
#print(df)
df.to_sql('weekly_stocks',engine)