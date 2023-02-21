from flask import Flask,request,jsonify #pip install flask
from flask_restful import Resource,Api,abort,reqparse #pip install flask-restful
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

app=Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"]='postgresql://postgres:c98xa5@localhost/flaskapi'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]=False
api=Api(app)
db=SQLAlchemy(app)
ma=Marshmallow(app)
app.app_context().push()

class TodoRest(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    task=db.Column(db.String(100))
    summary=db.Column(db.Text())

    def __init__(self,task,summary):
        self.task=task
        self.summary=summary

@app.route("/")
def home_page():
    return "Hello World"

class Hello(Resource):

    def get(self):
        return {'hello':'world'}
api.add_resource(Hello,'/user/')


class TodoRestSchema(ma.Schema):
    class Meta:
        fields=('id','task','summary') 

todo_schema=TodoRestSchema()
todos_schema=TodoRestSchema(many=True)

class TodoList(Resource):
    def get(self):
        all_todos=TodoRest.query.all()
        results=todos_schema.dump(all_todos)
        return jsonify(results)
    def post(self):
        task=request.json['task']
        summary=request.json['summary']
        todos=TodoRest(task,summary)
        db.session.add(todos)
        db.session.commit()
        return todo_schema.jsonify(todos)
        
class Todos(Resource):
    def get(self,id):
        todo=TodoRest.query.get(id)
        results=todo_schema.dump(todo)
        return jsonify(results)
        
    def put(self,id):
        todo=TodoRest.query.get(id)
        task=request.json['task']
        summary=request.json['summary']
        todo.task=task
        todo.summary=summary
        db.session.commit()
        results=todo_schema.dump(todo)
        return jsonify(results)
        
    def delete(self,id):
        todo=TodoRest.query.get(id)
        db.session.delete(todo)
        db.session.commit()
        results=todo_schema.dump(todo)
        return jsonify(results)
        
api.add_resource(TodoList, '/todos')
api.add_resource(Todos, '/todos/<int:id>')

if __name__=='__main__':
    app.run(debug=True)
