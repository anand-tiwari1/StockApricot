from flask import Flask
from flask_restful import Api, Resource
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
import json
import os
import pandas as pd

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
db = SQLAlchemy(app)
db_connect = create_engine('sqlite:///weekStock.db')
api = Api(app)


class WeeklyReport(Resource):
    def get(self):
        connection = db_connect.connect()

        query = connection.execute("""
                WITH temporaryTable(ticker,average,high,low)
                AS(SELECT ticker,ROUND(AVG(high),2) AS average,MAX(high),MIN(low) 
                FROM weekly_stocks GROUP BY ticker)
                SELECT ticker,high,low,average FROM temporaryTable; 
        """)
        result = {'data': [dict(zip(tuple(query.keys()), i)) for i in query.cursor]}
        print(type(result))

        ### converting to json string
        result = json.dumps(result, indent=4, separators=(',', ': '))
        print(result)

        ### Writing the report to weekly_report.csv
        df = pd.read_json(result)
        # df.to_csv(r"reports\weekly_report.csv", index=None)

        ### Returning the json response as a json object to the webservice
        return json.loads(result)


api.add_resource(WeeklyReport, '/generate_weekly_report')

if __name__ == "__main__":
    app.run(debug=True)
