#!/usr/bin/env python3

from flask import Flask, request, make_response, jsonify
from flask_migrate import Migrate

from models import db, Bakery, BakedGood

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def home():
    return '<h1>Bakery GET-POST-PATCH-DELETE API</h1>'

@app.route('/bakeries', methods=['GET', 'POST'])
def bakeries():
    
    if request.method == 'GET':
        bakeries = [bakery.to_dict() for bakery in Bakery.query.all()]
        return make_response(  bakeries,   200  )
    
    elif request.method == 'POST':
        bakery = Bakery(name=request.form.get('name'))
        db.session.add(bakery)
        db.session.commit()
        
        bakery_dict = bakery.to_dict()
        resp = make_response(bakery_dict, 201)

@app.route('/bakeries/<int:id>', methods=['GET', 'PATCH', 'DELETE'])
def bakery_by_id(id):
    
    if request.method == 'GET':
        bakery = Bakery.query.filter_by(id=id).first()
        bakery_serialized = bakery.to_dict()
        return make_response ( bakery_serialized, 200  )
    
    elif request.method == 'PATCH':
        bakery = Bakery.query.filter_by(id=id).first()
        for attr in request.form:
            setattr(bakery, attr, request.form.get(attr))
            
        db.session.add(bakery)
        db.session.commit()
        
        bakery_dict = bakery.to_dict()
        resp = make_response(bakery_dict, 200)
        return resp
    
    elif request.method == 'DELETE':
        bakery = Bakery.query.filter_by(id=id).first()
        
        db.session.delete(bakery)
        db.session.commit()
        resp_body = {
            'delete-success': True,
            'message': "Bakery Deleted"
        }
        resp = make_response(resp_body, 200)
        return resp
    
    
@app.route('/baked_goods', methods=['GET', 'POST'])
def baked_goods():

    if request.method == 'GET':
        baked_goods = [bg.to_dict() for bg in BakedGood.query.all()]
        resp = make_response(baked_goods, 200)
        return resp
    
    elif request.method == 'POST':
        baked_good = BakedGood(
            name=request.form.get('name'),
            price=request.form.get('price'),
            bakery_id=request.form.get('bakery_id')
        )
        db.session.add(baked_good)
        db.session.commit()

        baked_good_dict = baked_good.to_dict()
        resp = make_response(baked_good_dict, 201)
        return resp

@app.route('/baked_goods/<int:id>', methods=['GET', 'DELETE'])
def baked_goods_by_id(id):

    if request.method == 'GET':
        baked_good = BakedGood.query.filter(BakedGood.id == id).first()
        baked_good_dict = baked_good.to_dict()
        resp = make_response(baked_good_dict, 200)
        return resp
    
    elif request.method == 'DELETE':
        baked_good = BakedGood.query.filter(BakedGood.id == id).first()
        db.session.delete(baked_good)
        db.session.commit()

        resp_body = {
            'delete_success': True,
            'message': 'Baked Good Deleted'
        }
        resp = make_response(resp_body, 200)
        return resp
            

@app.route('/baked_goods/by_price')
def baked_goods_by_price():
    baked_goods_by_price = BakedGood.query.order_by(BakedGood.price.desc()).all()
    baked_goods_by_price_serialized = [
        bg.to_dict() for bg in baked_goods_by_price
    ]
    return make_response( baked_goods_by_price_serialized, 200  )
   

@app.route('/baked_goods/most_expensive')
def most_expensive_baked_good():
    most_expensive = BakedGood.query.order_by(BakedGood.price.desc()).limit(1).first()
    most_expensive_serialized = most_expensive.to_dict()
    return make_response( most_expensive_serialized,   200  )

if __name__ == '__main__':
    app.run(port=5555, debug=True)