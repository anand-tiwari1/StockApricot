from datetime import date, datetime
from flask import Flask
from config import Config
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy import desc
import json
import os
import csv
import pandas as pd

basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'weekStock.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
db_connect = create_engine('sqlite:///weekStock.db')
api = Api(app)

class StockModel(db.Model):
    id=db.Column(db.String(100),primary_key=True)
    ticker=db.Column(db.String(10),nullable=False)
    date=db.Column(db.String(100),nullable=False)
    high=db.Column(db.Float,nullable=False)
    low=db.Column(db.Float,nullable=False)
    high_diff=db.Column(db.Float,nullable=False)

    def __repr__(self):
        return f"Stock(id={self.id},ticker={self.ticker},date={self.date},high={self.high},low={self.low},high_diff={self.high_diff}"

schema_put_args = reqparse.RequestParser()
schema_put_args.add_argument("id", type=str, help="ID is required",required=True)
schema_put_args.add_argument("date", type=str, help="Date is required", required=True)
schema_put_args.add_argument("ticker", type=str, help="Ticker symbol", required=True)
schema_put_args.add_argument("high", type=float, help="Highest stock value", required=True)
schema_put_args.add_argument("low", type=float, help="Lowest stock value", required=True)
schema_put_args.add_argument("high_diff", type=float, help="Difference percentage of stock value", required=True)

schema_update_args = reqparse.RequestParser()
schema_update_args.add_argument("id", type=str, help="ID")
schema_update_args.add_argument("date", type=str, help="Date is required")
schema_update_args.add_argument("ticker", type=str, help="Ticker symbol")
schema_update_args.add_argument("high", type=float, help="Highest stock value")
schema_update_args.add_argument("low", type=float, help="Lowest stock value")
schema_update_args.add_argument("high_diff", type=float, help="Difference percentage of stock value")

resource_fields = {
    'id': fields.String,
    'ticker': fields.String,
	'date': fields.String,
	'high': fields.Float,
	'low': fields.Float,
    'high_diff': fields.Float
}


class WeeklyReport(Resource):
    def get(self):
        connection = db_connect.connect()

        ### SQL Query to get the desired result
        query=connection.execute("""
                WITH temporaryTable(ticker,average,high,low)
                AS(SELECT ticker,ROUND(AVG(high),2) AS average,MAX(high),MIN(low) 
                FROM weekly_stocks GROUP BY ticker)
                SELECT ticker,high,low,average FROM temporaryTable; 
        """)
        result = {'data': [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor]}
        print(type(result))

        ### converting to json string
        result=json.dumps(result,indent=4, separators=(',', ': '))
        print(result)

        ### Writing the report to weekly_report.csv
        df=pd.read_json(result)
        df.to_csv(r"reports\weekly_report.csv",index=None)

        ### Returning the json response as a json object to the webservice
        return json.loads(result)

api.add_resource(WeeklyReport, '/generate_weekly_report') 


if __name__=="__main__":
    app.run(debug=True)


