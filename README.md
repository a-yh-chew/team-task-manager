# team-task-manager
This is a simple task management system small businesses can use.
--------------------
After logging in with the default admin credentials: username = 'admin' and password = 'password'.

The following features are available to the admin:
  - Registering new users
  - Assigning a new task to a user
  - Viewing and modifying all tasks on the system
  - Viewing and modifying all tasks assigned to the current user (in this case the admin)
  - Generating summary reports as text files
  - Displaying the summary reports in the console
  - Changing login credentials (though the admin can only change their password)
  - Exiting the program
--------------------
After the admin has registered a new user, and said user successfully logs in.

The following features are available to non-admin users:
  - Registering new users
  - Assigning a new task to a user
  - Viewing all tasks on the system
  - Viewing and modifying all tasks assigned to the current user
  - Changing login credentials
  - Exiting the program

--------------------
users.txt
--------------------
User login credentials are stored in the users.txt file.
users.txt will be created on program launch if the file doesn't already exist.
The file by default includes the string 'admin;password' serving as the admin credentials.

User credentials are read line by line.
Each line represents a user, and includes their username and password separated by a ';'. 
It's important to note that because users.txt uses ';' to separate components, semicolons can't be included in usernames or passwords.  

--------------------
tasks.txt
--------------------
Tasks information are stored in the tasks.txt file.
tasks.txt will be created on program launch if the file doesn't already exist.
The file will be empty by default.

Tasks are read line by line.
Each line represents a task, and includes:
  - The name of the user the task is assigned to
  - Task title
  - Task description
  - Task due date
  - The date and time assigned
  - Whether the task is complete
  - Whether the task is overdue
    
These task components are separated by ';'.
Because tasks.txt uses ';' to separate task components, semicolons can't be included in any task components.  
