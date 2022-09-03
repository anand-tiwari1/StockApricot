# from datetime import datetime
# import requests
# base="http://127.0.0.1:5000/"
# data=[]
#
# with open("ticker_symbols.txt", "r") as f:
#         tickers= [(line.strip()).split() for line in f]
# #print(tickers)
#
# for ticker in tickers:
#     with open('data/'+str(ticker[0])+'.csv','r') as file:
#         info = file.readlines()
#     lastRow = info[-1]
#     lastRow = str(info[-1]).split(",")
#     #print(lastRow)
#     to_convert_to_date_format=lastRow[1]
#     lastRow[1]=to_convert_to_date_format[8:10]+'/'+to_convert_to_date_format[5:7]+'/'+to_convert_to_date_format[0:4]
#     #print(lastRow[1])
#     lastRow[8]=lastRow[8].strip('\n')
#     my_dict={"id":lastRow[8],"date":lastRow[1],"ticker":lastRow[6],
#         "high":round(float(lastRow[3]),2),"low":round(float(lastRow[4]),2),"high_diff":float(lastRow[7])}
#     data.append(my_dict)
#
# #print(data)
#
# for i in range(len(data)):
#     response=requests.put(base+"stock/"+str(data[i]["id"]),data[i])
#     print(response.json())
#
# input()
#
#
