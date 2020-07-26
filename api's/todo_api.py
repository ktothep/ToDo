from flask_restful import Api, Resource
from flask import Flask,request
from datetime import date

app=Flask(__name__)
api=Api(app)

todo_items=[]
class ToDo(Resource):

    def get(self,name):
     for task in todo_items:
        if name==task['name']:
            return "Task: {task}  Due Date: {duedate}   Created On: {createddate} ".format(task=task['task'],duedate=task['due_date'],createddate=task['created_date']),200
     else:
        return "No such Task Name in the ToDo list",200

    def delete(self,name):
        for task in todo_items:
            if name == task['name']:
              todo_items.remove(task)
              return "Task has been Deleted",200
        else:
            return "No such Task Name in the ToDo list", 200

class TodoPut(Resource):
    def put(self, id):
        data = request.get_json()
        name = data['name']
        task = data['task']
        due_date = data['duedate']
        for items in todo_items:
            if id == items['id']:
                    items['name']=name
                    items['task'] = task
                    items['due_date'] = due_date
        return "Task has been updated",201

class ToDoList(Resource):
    def get(self):
        return todo_items.__str__(),200

    def post(self):
        data=request.get_json()
        id=data['id']
        name=data['name']
        task=data['task']
        due_date=data['duedate']
        created_date=date.today()
        todo_items.append({"id":id,
                                   "name":name,
                                   "task":task,
                                   "due_date":due_date,
                                   "created_date":created_date})
        return "Task: {task} has been created in your ToDo list".format(task=task),201


api.add_resource(ToDoList,"/")
api.add_resource(ToDo,"/<string:name>")
api.add_resource(TodoPut,"/<int:id>")

app.run(port=8000)

