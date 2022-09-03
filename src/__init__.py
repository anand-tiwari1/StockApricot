from datetime import date, datetime
from flask import Flask
from config import Config
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, desc
import json
import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
                              'sqlite:///' + os.path.join(basedir, 'stock_model.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False


app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
db_connect = create_engine('sqlite:///stock_model.db')
api = Api(app)


class StockModel(db.Model):
    id = db.Column(db.String(100), primary_key=True)
    ticker = db.Column(db.String(10), nullable=False)
    date = db.Column(db.String(100), nullable=False)
    high = db.Column(db.Float, nullable=False)
    low = db.Column(db.Float, nullable=False)
    high_diff = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return f"Stock(id={self.id},ticker={self.ticker},date={self.date},high={self.high},low={self.low},high_diff={self.high_diff}"


schema_put_args = reqparse.RequestParser()
schema_put_args.add_argument("id", type=str, help="ID is required", required=True)
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


class Gainers(Resource):
    def get(self):
        connection = db_connect.connect()
        query = connection.execute("SELECT ticker,high_diff FROM stock_model ORDER BY high_diff DESC LIMIT 10;")
        result = {'data': [dict(zip(tuple(query.keys()), i)) for i in query.cursor]}
        result = json.dumps(result, indent=4, separators=(',', ': '))
        print(result)
        return json.loads(result)


class Losers(Resource):
    def get(self):
        connection = db_connect.connect()
        query = connection.execute("SELECT ticker,high_diff FROM stock_model ORDER BY high_diff ASC LIMIT 10;")
        result = {'data': [dict(zip(tuple(query.keys()), i)) for i in query.cursor]}
        result = json.dumps(result, indent=4, separators=(',', ': '))
        print(result)
        return json.loads(result)


api.add_resource(Gainers, '/get_top_gainers')
api.add_resource(Losers, '/get_top_losers')

if __name__ == "__main__":
    app.run(debug=True)
