# ToDo
A Todo Application for Task Management


1.Run the Application.

Base URL=localhost:8000

Note:Initial Todo list will be empty

For Getting Todo items:
Get Method on localhost:8000/


For Creating a Todo Item:
Post Method on localhost:8000/
JSON Body:
   {
   "id":2,
   "name":"Shop",
   "task":"Groceries for whole week",
   "duedate":"27/08/2020"
   }
   
For Deleting a Todo Item:
Delete Method on localhost:8000/{name}

For Updating a Todo Item:
Put method on localhost:8000/{id}
JSON Body:
  {
   "name":"Shop",
   "task":"Groceries for whole week",
   "duedate":"27/08/2020"
   }


   
   
   
