# ToDo
A Todo Application for Task Management

MongoDB:
    Port configured for MongoDB is 27017

1.Run the Application.

Base URL=0.0.0.0:5000

Note:Initial Todo list will be empty

For Getting Todo items:
Get Method on 0.0.0.0:5000/


For Creating a Todo Item:
Post Method on 0.0.0.0:5000/
JSON Body:
   {
   "name":"Shop",
   "task":"Groceries for whole week",
   "duedate":"27/08/2020"
   }
   
For Deleting a Todo Item:
Delete Method on 0.0.0.0:5000/{name}

For Updating a Todo Item:
Put method on 0.0.0.0:8000/{id}
JSON Body:
  {
   "name":"Shop",
   "task":"Groceries for whole week",
   "duedate":"27/08/2020"
   }

#Docker
Dockerfile is already present
- Execute the command:
docker build -t {name} .

- To run the container maker use of:
docker run -p 5000:5000 {name}
   
   
   
