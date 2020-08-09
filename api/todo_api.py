import configparser
from datetime import date

from flask import Flask, request, escape
from flask_restful import Api, Resource
from pymongo import MongoClient

parser = configparser.ConfigParser()
parser.read('configuration.ini')
mongo_config = parser['Database']['mongodb']
api_host = parser['api']['api_host']
api_port = parser['api']['port']

client = MongoClient(mongo_config)
app = Flask(__name__)
api = Api(app)

db = client.apidb


class ToDo(Resource):
    """
    This class is for api request with path parameters.
    It caters to get,delete,put reuest with path parameter: /name
    """

    @staticmethod
    def get(name):
        """
        :param name: of the task
        :return: 200 if task exist with task details and gives 404 if task not found
        """
        for task in db.todotable.find({"name": escape(name)}):
            taskid = task.get("_id")
            if taskid:
                return "Task: {task}  Due Date: {duedate}   Created On: {createddate} " \
                           .format(task=task.get("task"),
                                   duedate=task.get("due_date"),
                                   createddate=task.get("created_date")), 200
        return "No such Task Name in the ToDo list", 404

    @staticmethod
    def delete(name):
        """
        Deletes a particular task whose name is passed as a path parameter
        :param name: of the task
        :return:200 if task is found and deleted else throws 404
        """
        for task in db.todotable.find({"name": escape(name)}):
            taskid = task.get("_id")
            db.todotable.delete_one({"_id": taskid})
            return "Task has been Deleted", 200
        return "No such Task Name in the ToDo list", 404

    @staticmethod
    def put(name):
        """
         Edit a given task which is passed as a path parameter.
         Update task,duedate and name
         :param name of the task
         :return:201 if task has been updated successfully.404 if task mentioned does not exist
        """
        result = db.todotable.find({"name": escape(name)})
        for value in result:
            if value.get("_id"):
                data = request.get_json()
                task = data['task']
                due_date = data['duedate']
                query = {"name": name}
                updatevalues = {"$set": {"task": task, "due_date": due_date}}
                db.todotable.update_one(query, updatevalues)
                return "Task  has been updated", 201
        return "Task Name does not exist", 404


class ToDoList(Resource):
    """
    This class is for api request without path parameters.
    It caters to get and post request 
    """
    @staticmethod
    def get():
        """
        Fetch values from MongoDB and show all the task that are present.
        Values are returned in JSON Format
        :return 200 along with all the task present in the MongoDB
        """
        todo_items = []
        for result in db.todotable.find({}, {"_id": 0,
                                             "name": 1,
                                             "task": 1,
                                             "due_date": 1,
                                             "created_date": 1}):
            todo_items.append(result)
        return todo_items, 200

    @staticmethod
    def post():
        """
        This method is used for creating a task.It reads the values from JSON
        Insert them in mongodb
        return 201 if task has been created successfully
        """
        data = request.get_json()
        name = data['name']
        task = data['task']
        due_date = data['duedate']
        created_date = date.today().__str__()
        for value in db.todotable.find({"task": task}):
            if value.get("_id"):
                return "Task: {task} is already present in your ToDo list".format(task=task), 200
        db.todotable.insert_one({"name": name,
                                 "task": task,
                                 "due_date": due_date,
                                 "created_date": created_date})
        return "Task: {task} has been created in your ToDo list".format(task=task), 201


api.add_resource(ToDoList, "/")
api.add_resource(ToDo, "/<string:name>")

app.run(host=api_host, port=api_port)
