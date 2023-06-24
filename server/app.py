#!/usr/bin/env python3

from flask import Flask, make_response, jsonify
from flask_migrate import Migrate

from models import db, Bakery, BakedGood

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def index():
    return '<h1>Bakery GET API</h1>'

@app.route('/bakeries')
def bakeries():

    bakeries = Bakery.query.all()
    bakeries_serialized = [bakery.to_dict() for bakery in bakeries]

    response = make_response(
        bakeries_serialized,
        200
    )
    return response



@app.route('/bakeries/<int:id>', methods=['GET'])
def get_bakery(id):
    bakery = Bakery.query.get_or_404(id)
    bakery_data = {
        'id': bakery.id,
        'name': bakery.name,
        'location': bakery.location,
        'baked_goods': []
    }
    for baked_good in bakery.baked_goods:
        baked_good_data = {
            'id': baked_good.id,
            'name': baked_good.name,
            'price': baked_good.price
            # Additional baked good properties...
        }
        
        bakery_data['baked_goods'].append(baked_good_data)
    return jsonify(bakery_data)

@app.route('/baked_goods/by_price', methods=['GET'])
def get_baked_goods_by_price():
    baked_goods = BakedGood.query.order_by(BakedGood.price.desc()).all()
    baked_goods_list = []
    for baked_good in baked_goods:
        baked_good_data = {
            'id': baked_good.id,
            'name': baked_good.name,
            'price': baked_good.price
            # Additional baked good properties...
        }
        baked_goods_list.append(baked_good_data)
    return jsonify(baked_goods_list)

@app.route('/baked_goods/most_expensive', methods=['GET'])
def get_most_expensive_baked_good():
    baked_good = BakedGood.query.order_by(BakedGood.price.desc()).first()
    if baked_good:
        baked_good_data = {
            'id': baked_good.id,
            'name': baked_good.name,
            'price': baked_good.price
            # Additional baked good properties...
        }
        return jsonify(baked_good_data)
    else:
        return jsonify({'message': 'No baked goods found.'}), 404



if __name__ == '__main__':
    app.run(port=5555, debug=True)