'''This is a simple task management system small businesses can use.
--------------------
After logging in with the default admin credentials: username = 'admin' and
password = 'password'.

The following features are available to the admin:
    - Registering new users
    - Assigning a new task to a user
    - Viewing and modifying all tasks on the system
    - Viewing and modifying all tasks assigned to the current user
      (in this case the admin)
    - Generating summary reports as text files
    - Displaying the summary reports in the console
    - Changing login credentials
      (though the admin can only change their password)
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
This file is integral to the the functioning of the program.
User login credentials are stored in the users.txt file.
users.txt will be created on program launch if the file doesn't already exist.
The file by default includes the string 'admin;password' serving as the admin
credentials.

User credentials are read line by line.
Each line represents a user, and includes their username and password separated
by a ';'. 
It's important to note that because users.txt uses ';' to separate components,
semicolons can't be included in usernames or passwords.  

--------------------
tasks.txt
--------------------
This file is integral to the the functioning of the program.
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
Because tasks.txt uses ';' to separate task components, semicolons can't be
included in any task components.

--------------------
Constant variables
--------------------
After the datetime module is imported, the chosen date format throughout the
program is "%Y-%m-%d,%H:%M".

2:00 p.m. on the 29th of February 2024 would be formatted as: 2024-02-29,14:00

--------------------
Language notes
--------------------
- The use of 't' in this document is short for 'task'.
- 'curr' is short for 'current'.
- 'dt' is short for 'datetime'.

--------------------
Startup notes
--------------------
Use the following username and password to access the admin rights:
    - username: admin (this is not changeable).
    - password: password (this can be changed after logging in).

--------------------
Other notes
--------------------
If the 'overdue' status of task is incorrect (showing False instead of True).
This is due to current dt only being counted at the start of the following:
'view_all_tasks', 'view_my_tasks', 'generate_reports', and 'disp_stats'.
The fix to the incorrect status is to re-initialise one of these sections.

--------------------
To be added
--------------------
- Who assigned the task as a task component.
- Who and when last edited the task as a task component.
- Display how much time left to complete the tasks.
- Handling 'IndexError: list index out of range' for anomalies in .txt files.
'''
#---------------Importing Libraries---------------
import os
from datetime import datetime as dt
import functions

#---------------Constant Variables---------------
# This is our chosen date format.
DT_FORMAT = "%Y-%m-%d,%H:%M"

#---------------Main Structure---------------
# Create tasks.txt if it doesn't exist.
if not os.path.exists("tasks.txt"):
    with open("tasks.txt", "w") as default_file:
        pass
# Read each line of tasks.txt as an element in the 'tasks_data' list.
with open("tasks.txt", "r") as task_file:
    task_data = task_file.read().split("\n")
    task_data = [t for t in task_data if t != ""]

task_list = []
for task_string in task_data:
    curr_t = {}
    # Each component split by semicolon.
    t_comp = task_string.split(";")
    curr_t['username'] = t_comp[0]
    curr_t['title'] = t_comp[1]
    curr_t['description'] = t_comp[2]
    curr_t['due_date'] = dt.strptime(t_comp[3], DT_FORMAT)
    curr_t['assigned_date'] = dt.strptime(t_comp[4], DT_FORMAT)
    curr_t['completed'] = True if t_comp[5] == 'Yes' else False
    curr_t['overdue'] = True if not curr_t['completed'] and \
        dt.strptime(t_comp[3], DT_FORMAT) < dt.now() else False
    task_list.append(curr_t)

# Rewriting tasks.txt to update the 'overdue' status if there's any change.
with open("tasks.txt", "w") as task_file:
    task_list_to_write = []
    for t in task_list:
        t_comp = [
            t['username'],
            t['title'],
            t['description'],
            t['due_date'].strftime(DT_FORMAT),
            t['assigned_date'].strftime(DT_FORMAT),
            'Yes' if t['completed'] else 'No',
            'Yes' if t['overdue'] else 'No'
        ]
        task_list_to_write.append(";".join(t_comp))
    task_file.write("\n".join(task_list_to_write))

#---------------Login Section---------------
# Reads usernames and password from the users.txt file to allow a user to login.
# If there's no users.txt file, write one with a default admin account.
if not os.path.exists("users.txt"):
    with open("users.txt", "w") as default_file:
        default_file.write("admin;password")

# Read each line of users.txt as an element in the 'user_data' list.
with open("users.txt", "r") as user_file:
    user_data = user_file.read().split("\n")

# Convert user_data list into a dictionary.
username_password = {}
for user in user_data:
    username, password = user.split(";")
    username_password[username] = password

logged_in = False
while not logged_in:
    print("="*200)
    print("LOGIN")
    current_user = input("Username: ")
    current_pass = input("Password: ")
    if current_user not in username_password:
        print("-"*200)
        print("User does not exist.", end = " ")
        print("(Note: login is case and space sensitive)")
        continue
    elif username_password[current_user] != current_pass:
        print("-"*200)
        print("Wrong password.", end = " ")
        print("(Note: login is case and space sensitive)")
        continue
    else:
        print("-"*200)
        print("Login Successful!")
        logged_in = True

while True:
    if current_user == "admin":
        choice = input(f'''{"=" * 200}\nMAIN MENU\n{"-" * 200}
Select one of the following options below:
r - Registering a user
a - Adding a task
va - View all tasks
vm - View my tasks
gr - Generate reports
ds - Display statistics
c - Change login details
e - Exit
Enter letter/s: ''').lower()
    else:
        choice = input(f'''{"=" * 200}\nMAIN MENU\n{"-" * 200}
Select one of the following options below:
r - Registering a user
a - Adding a task
va - View all tasks
vm - View my tasks
c - Change login details
e - Exit
Enter letter/s: ''').lower()
    if choice == "r":
        functions.reg_user()
    elif choice == "a":
        functions.add_task()
    elif choice == "va":
        functions.view_all_tasks(current_user)
    elif choice == "vm":
        functions.view_my_tasks(current_user)
    elif current_user == "admin" and choice == "gr":
        functions.generate_report()
    elif current_user == "admin" and choice == "ds":
        functions.disp_stats()
    elif choice == "c":
        functions.edit_profile(current_user, current_pass)
    elif choice == "e":
        break
    else:
        print("-"*200)
        print("You must enter letter/s from the menu.", end = " ")
        print("(Note: choice input is space sensitive)")
print("-"*200)
print(f"Goodbye {current_user.capitalize()}!")
print("-"*200)
exit()
