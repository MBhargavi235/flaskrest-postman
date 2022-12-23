from flask import Flask, json,jsonify,request
from flask_sqlalchemy import SQLAlchemy
from marshmallow import Schema,fields

app=Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"]='postgresql://postgres:c98xa5@localhost/flaskapi'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]=False


db=SQLAlchemy(app)
app.app_context().push()

# id
#name
#description

class Products(db.Model):
    id=db.Column(db.Integer(),primary_key=True)
    title=db.Column(db.String(255),nullable=False)
    price=db.Column(db.Float(),nullable=False)
    description=db.Column(db.Text(),nullable=False)
    category=db.Column(db.String(50),nullable=False)
    image=db.Column(db.String(255),nullable=False)
    rating=db.Column(db.Float(),nullable=False)

    def __repr__(self):
        return self.name

    @classmethod
    def get_all(cls):
        return cls.query.all()
    
    @classmethod
    def get_by_id(cls,id):
        return cls.query.get_or_404(id)

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

class ProductsSchema(Schema):
    id=fields.Integer()
    title=fields.String()
    price=fields.Float()
    description=fields.String()
    category=fields.String()
    image=fields.String()
    rating=fields.Float()
    
@app.route('/products',methods=['GET'])
def get_all_products():
    products=Products.get_all()

    serializer=ProductsSchema(many=True)

    data=serializer.dump(products)

    return jsonify(
        data
    )


@app.route('/products',methods=['POST'])
def create_a_products():
    data=request.get_json()

    new_product=Products(
        title=data.get('title'),
        price=data.get('price'),
        description=data.get('description'),
        category=data.get('category'),
        image=data.get('image'),
        rating=data.get('rating')
    )

    new_product.save()

    serializer=ProductsSchema()

    data=serializer.dump(new_product)

    return jsonify(
        data
    ),201

@app.route('/products/<int:id>',methods=['GET'])
def get_products(id):
    products=Products.get_by_id(id)

    serializer=ProductsSchema()

    data=serializer.dump(products)

    return jsonify(
        data
    ),200

@app.route('/products/<int:id>',methods=['PUT'])
def update_products(id):
    products_to_update=Products.get_by_id(id)

    data=request.get_json()

    products_to_update.title=data.get('title')
    products_to_update.price=data.get('price'),
    products_to_update.description=data.get('description'),
    products_to_update.category=data.get('category'),
    products_to_update.image=data.get('image'),
    products_to_update.rating=data.get('rating')
    db.session.commit()

    serializer=ProductsSchema()
    products_data=serializer.dump(products_to_update)
    return jsonify(products_data),200

@app.route('/products/<int:id>',methods=['DELETE'])
def delete_recipe(id):
    products_to_delete=Products.get_by_id(id)

    products_to_delete.delete()

    return jsonify({"message":"Deleted"}),204


@app.errorhandler(404)
def not_found(error):
    return jsonify({"message":"Resource not found"}),404

@app.errorhandler(500)
def internal_server(error):
    return jsonify({"message":"There is a problem"}),500

if __name__ == '__main__':
    app.run(debug=True)
