from datetime import date, datetime
from flask import Flask
from config import Config
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine

import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config(object):
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
                              'sqlite:///' + os.path.join(basedir, 'stock_model.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False


app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
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

# db.drop_all()
# db.create_all()

resource_fields = {
    'id': fields.String,
    'ticker': fields.String,
    'date': fields.String,
    'high': fields.Float,
    'low': fields.Float,
    'high_diff': fields.Float
}


class Stocks(Resource):

    @marshal_with(resource_fields)
    def put(self, id):
        args = schema_put_args.parse_args()
        stock = StockModel(id=args['id'], ticker=args['ticker'], date=args['date'], high=args['high'], low=args['low'],
                           high_diff=args['high_diff'])
        db.session.add(stock)
        db.session.commit()
        return stock, 201


api.add_resource(Stocks, "/stock/<string:id>")

if __name__ == "__main__":
    app.run(debug=True)
