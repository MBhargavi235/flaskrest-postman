from flask import Flask,request
from flask_restful import Resource, Api,reqparse,abort
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:c98xa5@localhost/sample'
db = SQLAlchemy(app)
app.app_context().push()

class PersonDsetails(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(200))
    age = db.Column(db.Integer)

db.create_all()

class PersonResource(Resource):
    def get(self):
        people =PersonDsetails.query.all()
        result = []
        for person in people:
            result.append({'id': person.id, 'name': person.name, 'age': person.age})
        return result

    def post(self):
        data = request.json
        person = PersonDsetails(name=data['name'], age=data['age'])
        db.session.add(person)
        db.session.commit()
        return {'id': person.id, 'name': person.name, 'age': person.age}

class PersonUpAndDelete(Resource):
    def get(self,id):
        person = PersonDsetails.query.filter_by(id=id).first()
        return {'id': person.id, 'name': person.name, 'age': person.age}
    
    def put(self, id):
        person = PersonDsetails.query.filter_by(id=id).first()
        if not person:
            return {'message': 'Person not found'}, 404
        data = request.json
        person.name = data['name']
        person.age = data['age']
        db.session.commit()
        return {'id': person.id, 'name': person.name, 'age': person.age}

    def delete(self, id):
        person = PersonDsetails.query.filter_by(id=id).first()
        if not person:
            return {'message': 'Person not found'}, 404
        db.session.delete(person)
        db.session.commit()
        return {'message': 'Person deleted'}

api.add_resource(PersonResource,"/persons")
api.add_resource(PersonUpAndDelete,"/persons/<int:id>")

if __name__=='__main__':
    app.run(debug=True)
