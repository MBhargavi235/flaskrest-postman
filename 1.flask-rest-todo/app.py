from flask import Flask,request #pip install flask
from flask_restful import Resource,Api,abort,reqparse #pip install flask-restful

app=Flask(__name__)
api=Api(app)

@app.route("/")
def home_page():
    return "Hello World"

class Hello(Resource):

    def get(self):
        return {'hello':'world'}
api.add_resource(Hello,'/user/')

todos={
    1:{"task":"Write hello world program","summary":"Write the code using python"}
}
task_post_args=reqparse.RequestParser()
task_post_args.add_argument("task",type=str,help="Task is required",required=True)
task_post_args.add_argument("summary",type=str,help="Summary is required",required=True)

task_put_args=reqparse.RequestParser()
task_put_args.add_argument("task",type=str)
task_put_args.add_argument("summary",type=str)

class TodoList(Resource):
    def get(self):
        return todos
        
class Todos(Resource):

    def get(self,todo_id):
        return todos[todo_id]
        
    def post(self,todo_id):
        args=task_post_args.parse_args()
        if todo_id in todos:
            abort(409,'Task ID already taken')
        todos[todo_id]={"task":args['task'],"summary":args['summary']}
        return todos[todo_id]
        
    def put(self,todo_id):
        args=task_put_args.parse_args()
        if todo_id not in todos:
            abort(404,'Task does not exist cannot update')
        if args['task']:
            todos[todo_id]['task']=args['task']
        if args['summary']: 
            todos[todo_id]['summary']=args['summary']
        return "Updated successfully"
        
    def delete(self,todo_id):
        del todos[todo_id]
        return "task deleted successfully"
        
api.add_resource(TodoList, '/todos')
api.add_resource(Todos, '/todos/<int:todo_id>')

if __name__=='__main__':
    app.run(debug=True)
