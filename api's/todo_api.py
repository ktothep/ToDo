from datetime import date

from flask import Flask, request
from flask_restful import Api, Resource
from pymongo import MongoClient

client = MongoClient(port=27017)
app = Flask(__name__)
api = Api(app)

db = client.apidb


class ToDo(Resource):

    def get(self, name):
        for task in db.todotable.find({"name":name}):
            id=task.get("_id")
            if id:
                return "Task: {task}  Due Date: {duedate}   Created On: {createddate} ".format(task=task.get("task"),
                                                                                               duedate=task.get("due_date"),
                                                                                               createddate=task.get("created_date")), 200
        else:
            return "No such Task Name in the ToDo list", 200

    def delete(self, name):
        for task in db.todotable.find({"name":name}):
            id=task.get("_id")
            db.todotable.delete_one({"_id":id})
            return "Task has been Deleted", 200
        else:
            return "No such Task Name in the ToDo list", 200

    def put(self, name):
        result=db.todotable.find({"name":name})
        for x in result:
            if x.get("_id"):
                data = request.get_json()
                task = data['task']
                due_date = data['duedate']
                query= {"name": name}
                updatevalues={"$set":{"task":task,"due_date":due_date}}
                db.todotable.update_one(query,updatevalues)
                return "Task  has been updated", 201
            else:
                return "Task Name does not exist",304


class ToDoList(Resource):
    def get(self):
        todo_items = []
        for result in db.todotable.find({},{"_id":0,"name":1,"task":1,"due_date":1,"created_date":1}):
            todo_items.append(result)
        return todo_items


    def post(self):
        data = request.get_json()
        name = data['name']
        task = data['task']
        due_date = data['duedate']
        created_date = date.today().__str__()
        for x in db.todotable.find({"task":task}):
            if x.get("_id"):
                return "Task: {task} is already present in your ToDo list".format(task=task), 201
        else:
            db.todotable.insert_one({"name": name, "task": task, "due_date": due_date, "created_date": created_date})
            return "Task: {task} has been created in your ToDo list".format(task=task), 201




api.add_resource(ToDoList, "/")
api.add_resource(ToDo, "/<string:name>")

app.run(host="0.0.0.0", port=5000)
