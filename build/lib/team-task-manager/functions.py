'''This module primarily contains the functions that allow a simple team task
management program to work.
--------------------
Functions:

    Recurrent:

        semicolon_found(*args) -> string, bool:
            Checks if arguments include semicolon.
        character_exceed(*args) -> strings, bool:
            Checks if arguments exceed the length of 163 characters.
    
    Additive:

        reg_user: Adds a new user onto the system.
        add_task: Adds a new task onto the system.

    Viewing/modifying:

        view_all_tasks(current_user): Displays all tasks on the system to the
            console.
        manage_t(t_choice, all_t_index): Displays a chosen task and presents
            task managing options. Admin only.
        mark_complete(t_choice, all_t_index): Changes whether a task is or
            isn't complete. Admin only.
        change_person(t_choice, all_t_index): Changes the user that a task is
            assigned to. Admin only.
        change_date(t_choice, all_t_index): Changes the due date of a tasks.
            Admin only.

        view_my_tasks(current_user): Displays all tasks on the system assigned
            to the current user to the console.
        vm_manage_t(t_choice, index_dict, all_t_index): Displays a chosen task
            and presents task managing options.
        vm_mark_complete(t_choice, index_dict, all_t_index): Changes whether a
            task is or isn't complete.
        vm_change_person(t_choice, index_dict, all_t_index): Changes the user
            that a task is assigned to.
        vm_change_date(t_choice, index_dict, all_t_index): Changes the due date
            of a tasks.

    Summary:

        generate_report: Generates a task overview and user overview file.
            Admin only. 
        disp_stats: Displays an overview of all tasks and users to the console.
            Admin only.

    Modifying login:
        edit_profile(current_user, current_pass): Presents the login editing
            options.
        edit_name(current_user, current_pass): Changes the user's username.
        edit_pass(current_user): Changes the user's password.

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
task_overview.txt
--------------------
This file displays an overview of all tasks in tasks.txt, and is
generated/rewritten when generate_report is called by the admin. 

Displays:
    - The total number of task
    - The number of completed tasks
    - The number of incomplete and overdue tasks
    - The percentage of incomplete tasks
    - The percentage of overdue tasks

--------------------
user_overview.txt
--------------------
This file displays an overview of all users in users.txt and the tasks 
assigned to them in tasks.txt, and is generated/rewritten when generate_report
is called by the admin. 

Displays:
    - The number of users
    - The number of tasks generated and tracked
    - The following information per user:
        - Username
        - Number of tasks
        - Percentage of all tasks assigned to this user
        - Percentage of tasks completed
        - Percentage of tasks incomplete
        - Percentage of tasks incomplete and overdue

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
- 'u' is short for 'user'.
- 'vm' is short for 'view my'.
- 'disp' is short for 'display'.
- 'oview' is short for 'overview'.
- 'per' is short for 'percent'.
'''
#---------------Importing Libraries---------------
from datetime import datetime as dt
from math import floor

#---------------Constant Variables---------------
# This is our chosen date format.
DT_FORMAT = "%Y-%m-%d,%H:%M"

#---------------Functions---------------
def semicolon_found(*args):
    '''Checks if arguments include semicolon. 

    (This is important because semicolons in this program are used to separate
    task_list elements. Semicolons will disrupt the functionality
    of this program if accepted.)

            Parameters:
                    *args: Variable length argument list.
            
            Returns:
                    bool: 'Entry is invalid' notice and True for success.
                          False otherwise.
    '''
    if ";" in args:
        print("-"*200)
        print("Your entry is invalid.", end = " ")
        print("(Note: please do not enter inputs containing ';')")
        return True
    else:
        return False


def character_exceed(args):
    '''Checks if arguments exceed the length of 163 characters.

    (The 163 character limit is for the sake of presentation.
    To stay within the 200 character length border lines.
    This maximum length was determined by how the program feedback after a
    username (edit_name) or password (edit_pass) change takes up 37 characters
    in the console and the remaining space is shared with said new username or
    password.)

            Parameters:
                    args: An argument.
            
            Returns:
                    bool: 'Input too long' notice and True for success.
                          False otherwise.
    '''
    if len(args) > 163:
        print("-"*200)
        print("Input length was too long.", end = " ")
        print("(Note: input should be 163 characters maximum)")
        return True
    else:
        return False


def reg_user():
    '''Reads users.txt to recognise the existing list of users.
    But primarily, adds a new user to the users.txt file.
    
    Prompts the user for the following:
        - A new username.
        - Password.
        - Password confirmation.

    Conditions required for user registration:
        - The username mustn't already exists in the users.txt file.
        - The new password and confirmed password must match.
        - The username and password can't exceed 163 characters or include ';'.

    If any of the above criteria are not met the user is notified of this and
    returned to the main menu.
    
    If the above criteria are met, the new user is added into users.txt as
    "username;password" on a new line. The user is notified that a new user has
    been added and is returned to the main menu.
    '''
    with open("users.txt", "r") as user_file:
        user_data = user_file.read().split("\n")

    username_password = {}
    for user in user_data:
        username, password = user.split(";")
        username_password[username] = password

    print("="*200)
    print("REGISTERING A USER")
    print("-"*200)
    new_username = input("New Username: ")
    new_password = input("New Password: ")
    confirm_password = input("Confirm Password: ")
    if new_username in username_password:
        print("-"*200)
        print("This username is taken.", end = " ")
        print("(Note: usernames must be unique)")
        print("No new user was added.")
    elif semicolon_found(new_username, new_password):
        print("No new user was added.")
    elif new_password != confirm_password:
        print("-"*200)
        print("Passwords do no match.", end = " ")
        print("(Note: login is case and space sensitive)")
        print("No new user was added.")
    elif character_exceed(new_username):
        print("No new user was added.")
    elif character_exceed(new_password):
        print("No new user was added.")
    else:
        username_password[new_username] = new_password
        with open("users.txt", "w") as reg_file:
            user_data = []
            for key in username_password:
                user_data.append(f"{key};{username_password[key]}")
            reg_file.write("\n".join(user_data))
        print("-"*200)
        print(f"New user '{new_username}' was added.")


def add_task():
    '''Reads users.txt to recognise the existing list of users.
    Reads tasks.txt to recognise the existing list of tasks.
    But primarily, adds a new task to the tasks.txt file.

    Prompts a user for the following: 
        - A username of the person whom the task is assigned to,
        - A title of a task
        - A description of the task.
        - The due date of the task.

    Conditions required for task assignment:
        - User inputs can't exceed 163 characters or include ';'.
        - The chosen due date must not have already passed and
          match the specified format.
    
    If any of the above criteria are not met the user is notified of this and
    returned to the main menu.

    If the above criteria are met, the task is added into tasks.txt.
    With 'No' to indicate that the task is not complete.
    And includes an indication of whether the task is overdue.

    Feedback to user:
        - The user that has been given the new task.
        - The date and time set.
        - The date and time due.
        - The time (days and hours) given to complete the task.

    The user then returns to the main menu.
    '''
    with open("users.txt", "r") as user_file:
        user_data = user_file.read().split("\n")

    username_password = {}
    for user in user_data:
        username, password = user.split(";")
        username_password[username] = password

    with open("tasks.txt", "r") as task_file:
        task_data = task_file.read().split("\n")
        task_data = [t for t in task_data if t != ""]

    task_list = []
    for task_string in task_data:
        curr_t = {}
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

    print("="*200)
    print("ADDING A TASK")
    print("-"*200)
    task_username = input("Username of the person assigned this task: ")
    if task_username not in username_password:
        print("-"*200)
        print("User does not exist. Please enter a valid username.")
        print("No new task was added.")
    else:
        task_title = input("Title of Task: ")
        if semicolon_found(task_title):
            print("No new task was added.")
        elif character_exceed(task_title):
            print("No new task was added.")
        else:
            task_description = input("Description of Task: ")
            if semicolon_found(task_description):
                print("No new task was added.")
            elif character_exceed(task_description):
                print("No new task was added.")
            else:
                while True:
                    try:
                        task_due_date = input("Due date (YYYY-MM-DD,hh:mm): ")
                        task_due_date = dt.strptime(task_due_date, DT_FORMAT)
                        if task_due_date < dt.now():
                            print("-"*200)
                            print("You are unable to assign a", end = " ")
                            print("due date that has already passed.")
                            print("No new task was added.")
                            break
                        else:
                            new_task = {
                                'username': task_username,
                                'title': task_title,
                                'description': task_description,
                                'due_date': task_due_date,
                                'assigned_date': dt.now(),
                                'completed': False,
                                'overdue': True if task_due_date < dt.now() else False
                            }
                            task_list.append(new_task)
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
                            print("-"*200)
                            print(task_username.capitalize(), end =" ")
                            print(f"has been assigned a new task.")
                            print(f"Set on: {dt.now().strftime(DT_FORMAT)}.")
                            print(f"Due by: {task_due_date.strftime(DT_FORMAT)}.")
                            # Calculate and format the time given to complete.
                            time_diff = task_due_date - dt.now()
                            seconds = time_diff.total_seconds()
                            days = divmod(seconds, 86400)
                            hours = divmod(days[1], 3600)
                        print(f'''Approximate time given to complete the task:
{floor(days[0])} Days and {floor(hours[0])} hours.''')
                    except ValueError:
                        print("-"*200)
                        print("Invalid date format.", end = " ")
                        print("Please use the format specified.")
                        print("No new task was added.")
                    break


def view_all_tasks(current_user):
    '''Reads and rewrites tasks.txt in case the overdue status of a task changes.
    But primarily, reads and prints all tasks from task.txt to the console.

    Admin-only:
        - Can select a task they want to manage (via index).
        - Or they can return to the menu (via entering '-1').
        - After selecting a task they proceed to the manage_t menu.
    
    Otherwise users are returned to the main menu if:
        - They aren't the admin.
        - If there are no tasks.
    '''
    with open("tasks.txt", "r") as task_file:
        task_data = task_file.read().split("\n")
        task_data = [t for t in task_data if t != ""]

    task_list = []
    for task_string in task_data:
        curr_t = {}
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

    while True:
        t_choice = ""
        while t_choice != -1:
            try:
                print("="*200)
                print("VIEW ALL TASKS")
                # Enumerate through task_list to index all tasks.
                all_t_index = {}
                for index, t in enumerate(task_list, start = 1):
                    all_t_index[index] = t
                    print("-"*200)  # Capitalise the strings displayed.
                    disp = f"Task number:\t  {index}\n"
                    disp += f"Task:\t\t  {t['title'].capitalize()}\n"
                    disp += f"Task Description: {t['description'].capitalize()}\n"
                    disp += f"Assigned to:\t  {t['username'].capitalize()}\n"
                    disp += f"Date Assigned:\t  {t['assigned_date'].strftime(DT_FORMAT)}\n"
                    disp += f"Due Date: \t  {t['due_date'].strftime(DT_FORMAT)}\n"
                    disp += f"Completed:\t  {'Yes' if t['completed'] else 'No'}\n"
                    disp += f"Overdue:\t  {'Yes' if t['overdue'] else 'No'}"
                    print(disp)
                print("-"*200)
                print(f"There are a total of {len(task_list)} tasks.")
                if current_user != "admin":
                    break
                elif len(task_list) == 0:
                    break
                else:
                    print("-"*200)  # Must cast vm_t_choice as an integer.
                    t_choice =  int(input('''Please enter the number of the \
task you would like to manage (or enter '-1' to return to the main menu): '''))
                    # Only if 't_choice' is within the index of tasks.
                    # The user proceeds to the task management options.
                    if t_choice in all_t_index:
                        manage_t(t_choice, all_t_index)
                    elif t_choice == -1:
                        break
                    else:
                        print("-"*200)
                        print("You must enter a valid number.")
            except ValueError:  # Error handling for non integer t_choice.
                print("-"*200)
                print("You must enter a valid whole number.")
        print("-"*200)
        print("Returning you to the main menu.")
        break


def manage_t(t_choice, all_t_index):
    '''Displays the task that the admin chose to manage, and the options to:
        - Mark the task as complete
        - Change the user the task is assigned to
        - Change the due date of the task
        - Return to view the other tasks

            Parameters:
                    t_choice (int): A number matching a key in all_t_dict.

                    all_t_index (dict): Dictionary matching an index number
                        to a task in tasks.txt.
                        A task is a dictionary of task components.
    '''
    t = all_t_index.get(t_choice)
    print("="*200)
    print("MANAGE TASK")
    while True:
        manage_choice = ""
        while manage_choice != "v":
            print("-"*200)
            print("You have chosen to manage the task below:")
            print("-"*200)
            disp = f"Task: \t\t  {t['title'].capitalize()}\n"
            disp += f"Task Description: {t['description'].capitalize()}\n"
            disp += f"Assigned to: \t  {t['username'].capitalize()}\n"
            disp += f"Date Assigned: \t  {t['assigned_date'].strftime(DT_FORMAT)}\n"
            disp += f"Due Date: \t  {t['due_date'].strftime(DT_FORMAT)}\n"
            disp += f"Completed:\t  {'Yes' if t['completed'] else 'No'}\n"
            disp += f"Overdue:\t  {'Yes' if t['overdue'] else 'No'}"
            print(disp)
            manage_choice = input(f'''{"-" * 200}\nWhat do you want to do?
Select one of the following options below:
m - Mark this task as complete
u - Change the user this task is assigned to
d - Change the due date of this task
v - View my other tasks
Enter a letter: ''').lower()
            if manage_choice == "m":
                mark_complete(t_choice, all_t_index)
                break
            elif manage_choice == "u":
                change_person(t_choice, all_t_index)
                break
            elif manage_choice == "d":
                change_date(t_choice, all_t_index)
                break
            elif manage_choice == "v":
                break
            else:
                print("-"*200)
                print("You must enter a letter from the menu.", end = " ")
                print("(Note: choice input is space sensitive)")
        print("-"*200)
        print("Returning to view the other tasks.")
        break


def mark_complete(t_choice, all_t_index):
    '''Allows the admin to change the completeness status of the chosen task.
    If the task was marked as complete it will change to incomplete,
    whereas if it was marked as incomplete it will change to complete.
    A task not yet marked as overdue while marked as complete can not be
    marked as overdue even after the due date has passed. Though, if a task is
    marked as overdue and then marked as complete said task would still be
    marked as overdue.    
    These changes will be reflected in the console and tasks.txt.
    After the completeness status has been changed the admin is notified of
    this and returned to view all tasks on the system.

    Or the admin can choose to return to view the other task managing options,
    leaving the completeness status unchanged.

            Parameters:
                    t_choice (int): A number matching a key in all_t_dict.

                    all_t_index (dict): Dictionary matching an index number
                        to a task in tasks.txt.
                        A task is a dictionary of task components.
    '''
    print("-"*200)
    print("CHANGE COMPLETION STATUS")
    while True:
        mark_choice = ""
        while mark_choice != "r":
            print("-"*200)
            mark_choice =  input('''Please enter 'c' to change the completion\
 status of the task (changing 'Yes' to 'No', or changing 'No' to 'Yes') (or\
 enter 'r' to return to the task managing options):\n''').lower()
            if mark_choice == "c":
                for index, t in all_t_index.items():
                    if index == t_choice:
                        if t['completed']:
                            t['completed'] = False
                        else:
                            t['completed'] = True
                with open("tasks.txt", "w") as task_file:
                    task_list_to_write = []
                    for t in all_t_index.values():
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
                print("-"*200)
                print("The completion status of the task has been changed.")
                break
            elif mark_choice == "r":
                break
            else:
                print("-"*200)
                print("You must enter a valid letter.", end = " ")
                print("(Note: choice input is space sensitive)")
        break


def change_person(t_choice, all_t_index):
    '''Reads users.txt to recognise the existing list of users.
    But primarily, allows the admin to enter the name of the user they want the
    task reassigned to. This change will be reflected in the console and
    tasks.txt from this point onwards. After the task has been reassigned the
    admin is notified of this and returned to view all tasks on the system.

    Conditions required for task reassignment:
        - The task is marked as incomplete.
        - The given username exists in users.txt.
        - The user is different from the user already assigned to the task.

    While the chosen task is marked as complete the task can not be reassigned
    to a different user. Therefore, before changing who the task is assigned to
    the admin or the user currently assigned to the task must mark the task as
    incomplete.
    
    If any of the above criteria are not met the admin is notified this and
    returned to view all tasks on the system.

            Parameters:
                    t_choice (int): A number matching a key in all_t_dict.

                    all_t_index (dict): Dictionary matching an index number
                        to a task in tasks.txt.
                        A task is a dictionary of task components.
    '''
    with open("users.txt", "r") as user_file:
        user_data = user_file.read().split("\n")

    username_password = {}
    for user in user_data:
        username, password = user.split(";")
        username_password[username] = password

    if all_t_index[t_choice]['completed']:
        print("-"*200)
        print("The user assigned to a task can not be changed", end = " ")
        print("if the task has been marked as complete.")
    else:
        print("-"*200)
        print("REASSIGN TASK")
        print("-"*200)
        reassign_user =  input('''Please enter the username of the user\
 you want to reassign the task to:\n''')
        if reassign_user in username_password:
            if reassign_user == all_t_index[t_choice]['username']:
                print("-"*200)
                print(f"The task is already assigned to {reassign_user}.")
            else:
                for index, t in all_t_index.items():
                    if index == t_choice:
                        t['username'] = reassign_user
                with open("tasks.txt", "w") as task_file:
                    task_list_to_write = []
                    for t in all_t_index.values():
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
                print("-"*200)
                print(f"The task has been reassigned to {reassign_user}.")
        else:
            print("-"*200)
            print("This username does not exist on the system.", end = " ")
            print("(Note: input is case and space sensitive)")
            print("No task was reassigned")


def change_date(t_choice, all_t_index):
    '''Allows the admin to enter a new due date they want to assign to a task.
    Consequently, if said new due date changes how an overdue task is now
    not overdue this change will be reflected both in the console and tasks.txt
    from this point in time and onwards. After the task due date is changed
    the admin is notified of this and returned to view all tasks on the system.

    Conditions required for changing task due date:
        - The task is marked as incomplete.
        - The given due date has not already passed.
        - The given due date is different from the due date already assigned
          to the task.

    While the chosen task is marked as complete the due date of a task can't be
    changed. Therefore, before changing the due date of the task the admin or
    the user currently assigned to the task must mark the task as incomplete.
    
    If any of the above criteria are not met the admin is notified this and
    returned to view all tasks on the system.

            Parameters:
                    t_choice (int): A number matching a key in all_t_dict.

                    all_t_index (dict): Dictionary matching an index number
                        to a task in tasks.txt.
                        A task is a dictionary of task components.
    '''
    if all_t_index[t_choice]['completed']:
        print("-"*200)
        print("The due date of a task can not be changed", end = " ")
        print("if the task has been marked as complete.")
    else:
        print("-"*200)
        print("CHANGE DUE DATE")
        while True:
            try:
                print("-"*200)
                new_date =  input('''Please enter the new due date of the task\
 (YYYY-MM-DD,hh:mm):\n''')
                new_date = dt.strptime(new_date, DT_FORMAT)       
                if new_date == all_t_index[t_choice]['due_date']:
                    print("-"*200)
                    print("The task due date is already", end = " ")
                    print(f"{new_date.strftime(DT_FORMAT)}.")
                    break
                elif new_date < dt.now():
                    print("-"*200)
                    print("You are unable to assign a due date", end = " ")
                    print("that has already passed.")
                    break
                else:
                    # Change 'due_date' and 'overdue' status of the task.
                    for index, t in all_t_index.items():
                        if index == t_choice:
                            t['due_date'] = new_date
                            t['overdue'] = True if new_date < dt.now() else False
                    with open("tasks.txt", "w") as task_file:
                        task_list_to_write = []
                        for t in all_t_index.values():
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
                    print("-"*200)
                    print("The task due date has been changed to", end = " ")
                    print(f"{new_date.strftime(DT_FORMAT)}.")
                    break
            except ValueError:
                print("-"*200)
                print("Invalid date format.", end = " ")
                print("Please use the format specified.")
            break


def view_my_tasks(current_user):
    '''Reads and rewrites tasks.txt in case the overdue status of a task changes.
    But primarily, reads and prints the current user's tasks from task.txt
    to the console.

    All users:
        - Can select a task they want to manage (via index).
        - Or they can return to the menu (via entering '-1').
        - After selecting a task they proceed to the manage_t menu.
    
    Otherwise users are returned to the main menu if:
        - If there are no tasks assigned to them.
    '''
    with open("tasks.txt", "r") as task_file:
        task_data = task_file.read().split("\n")
        task_data = [t for t in task_data if t != ""]

    task_list = []
    for task_string in task_data:
        curr_t = {}
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

    while True:
        t_choice = ""
        while t_choice != -1:
            try:
                print("="*200)
                print("VIEW MY TASKS")
                # Enumerate through task_list to index all tasks.
                # Enumerate through all_t_index to index user-specific tasks.
                # Make dictionary of 'user-specific index' and 'overall index'.
                all_t_index = {}
                my_index = 0
                index_dict = {}
                for index, t in enumerate(task_list, start = 1):
                    all_t_index[index] = t
                    if t['username'] == current_user:
                        my_index += 1
                        index_dict[my_index] = index
                        print("-"*200)
                        disp = f"Task number:\t  {my_index}\n"
                        disp += f"Task:\t\t  {t['title'].capitalize()}\n"
                        disp += f"Task Description: {t['description'].capitalize()}\n"
                        disp += f"Assigned to:\t  {t['username'].capitalize()}\n"
                        disp += f"Date Assigned:\t  {t['assigned_date'].strftime(DT_FORMAT)}\n"
                        disp += f"Due Date: \t  {t['due_date'].strftime(DT_FORMAT)}\n"
                        disp += f"Completed:\t  {'Yes' if t['completed'] else 'No'}\n"
                        disp += f"Overdue:\t  {'Yes' if t['overdue'] else 'No'}"
                        print(disp)
                print("-"*200)
                print(f"There are a total of {my_index} tasks for you.")
                if my_index == 0:
                    break
                else:
                    print("-"*200)
                    t_choice =  int(input('''Please enter the number of the\
 task you would like to manage or enter '-1' to return to the main menu:\n'''))       
                    if t_choice in index_dict:
                        vm_manage_t(t_choice,index_dict, all_t_index)
                    elif t_choice == -1:
                        break
                    else:
                        print("-"*200)
                        print("You must enter a valid number.")
            except ValueError:
                print("-"*200)
                print("You must enter a valid whole number.")
        print("-"*200)
        print("Returning you to the main menu.")
        break


def vm_manage_t(t_choice, index_dict, all_t_index):
    '''Displays the task assigned to them that the user chose to manage,
    and the options to:
        - Mark the task as complete.
        - Change the user the task is assigned to.
        - Change the due date of the task.
        - Return to view the other tasks assigned to them.

            Parameters:
                    t_choice (int): A number matching a key in index_dict.

                    index_dict (dict): Dictionary matching an index number of
                        user-specific tasks in tasks.txt to an index number of
                        all tasks in tasks.txt.

                    all_t_index (dict): Dictionary matching an index number
                        to a task in tasks.txt.
                        A task is a dictionary of task components.
    '''
    t = all_t_index.get(index_dict[t_choice])
    print("="*200)
    print("MANAGE TASK")
    while True:
        manage_choice = ""
        while manage_choice != "v":
            print("-"*200)
            print("You have chosen to manage the task below:")
            print("-"*200)
            disp = f"Task: \t\t  {t['title'].capitalize()}\n"
            disp += f"Task Description: {t['description'].capitalize()}\n"
            disp += f"Assigned to: \t  {t['username'].capitalize()}\n"
            disp += f"Date Assigned: \t  {t['assigned_date'].strftime(DT_FORMAT)}\n"
            disp += f"Due Date: \t  {t['due_date'].strftime(DT_FORMAT)}\n"
            disp += f"Completed:\t  {'Yes' if t['completed'] else 'No'}\n"
            disp += f"Overdue:\t  {'Yes' if t['overdue'] else 'No'}"
            print(disp)
            manage_choice = input(f'''{"-" * 200}\nWhat do you want to do?
Select one of the following options below:
m - Mark this task as complete
u - Change the user this task is assigned to
d - Change the due date of this task
v - View my other tasks
Enter a letter: ''').lower()
            if manage_choice == "m":
                vm_mark_complete(t_choice,index_dict, all_t_index)
                break
            elif manage_choice == "u":
                print("choice u")
                vm_change_person(t_choice,index_dict, all_t_index)
                break
            elif manage_choice == "d":
                print("choice d")
                vm_change_date(t_choice,index_dict, all_t_index)
                break
            elif manage_choice == "v":
                break
            else:
                print("-"*200)
                print("You must enter a letter from the menu.", end = " ")
                print("(Note: choice input is space sensitive)")
        print("-"*200)
        print("Returning to view the other tasks.")
        break


def vm_mark_complete(t_choice, index_dict, all_t_index):
    '''Allows the user to change the completeness status of the chosen task.
    If the task was marked as complete it will change to incomplete,
    whereas if it was marked as incomplete it will change to complete.
    A task not yet marked as overdue while marked as complete can not be
    marked as overdue even after the due date has passed. Though, if a task is
    marked as overdue and then marked as complete said task would still be
    marked as overdue.    
    These changes will be reflected in the console and tasks.txt.
    After the completeness status has been changed the user is notified of this
    and returned to view all tasks assigned to them on the system.

    Or the user can choose to return to view the other task managing options,
    leaving the completeness status unchanged.

            Parameters:
                    t_choice (int): A number matching a key in index_dict.

                    index_dict (dict): Dictionary matching an index number of
                        user-specific tasks in tasks.txt to an index number of
                        all tasks in tasks.txt.

                    all_t_index (dict): Dictionary matching an index number
                        to a task in tasks.txt.
                        A task is a dictionary of task components.
    '''
    print("-"*200)
    print("CHANGE COMPLETION STATUS")
    while True:
        mark_choice = ""
        while mark_choice != "r":
            print("-"*200)
            mark_choice =  input('''Please enter 'c' to change the completion\
 status of the task (changing 'Yes' to 'No', or changing 'No' to 'Yes') (or\
 enter 'r' to return to the task managing options):\n''').lower()
            if mark_choice == "c":
                for index, t in all_t_index.items():
                    if index == index_dict[t_choice]:
                        if t['completed']:
                            t['completed'] = False
                        else:
                            t['completed'] = True
                with open("tasks.txt", "w") as task_file:
                    task_list_to_write = []
                    for t in all_t_index.values():
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
                print("-"*200)
                print("The completion status of the task has been changed.")
                break
            elif mark_choice == "r":
                break
            else:
                print("-"*200)
                print("You must enter a valid letter.", end = " ")
                print("(Note: choice input is space sensitive)")
        break


def vm_change_person(t_choice, index_dict, all_t_index):
    '''Reads users.txt to recognise the existing list of users.
    But primarily, allows the user to enter the name of the user they want the
    task reassigned to. This change will be reflected in the console and
    tasks.txt from this point onwards. After the task has been reassigned the
    current user is notified of this and returned to view all tasks assigned to
    them on the system.

    Conditions required for task reassignment:
        - The task is marked as incomplete.
        - The given username exists in users.txt.
        - The user is different from the user already assigned to the task.

    While the chosen task is marked as complete the task can not be reassigned
    to a different user. Therefore, before changing who the task is assigned to
    the admin or the user currently assigned to the task must mark the task as
    incomplete.
    
    If any of the above criteria are not met the user is notified this and
    returned to view all tasks assigned to them on the system.

            Parameters:
                    t_choice (int): A number matching a key in index_dict.

                    index_dict (dict): Dictionary matching an index number of
                        user-specific tasks in tasks.txt to an index number of
                        all tasks in tasks.txt.

                    all_t_index (dict): Dictionary matching an index number
                        to a task in tasks.txt.
                        A task is a dictionary of task components.
    '''
    with open("users.txt", "r") as user_file:
        user_data = user_file.read().split("\n")

    username_password = {}
    for user in user_data:
        username, password = user.split(";")
        username_password[username] = password

    if all_t_index[index_dict[t_choice]]['completed']:
        print("-"*200)
        print("The user assigned to a task can not be changed", end = " ")
        print("if the task has been marked as complete.")
    else:
        print("-"*200)
        print("REASSIGN TASK")
        print("-"*200)
        reassign_user =  input('''Please enter the username of the user\
 you want to reassign the task to:\n''')
        if reassign_user in username_password:
            if reassign_user == all_t_index[index_dict[t_choice]]['username']:
                print("-"*200)
                print(f"The task is already assigned to {reassign_user}.")
            else:
                for index, t in all_t_index.items():
                    if index == index_dict[t_choice]:
                        t['username'] = reassign_user
                with open("tasks.txt", "w") as task_file:
                    task_list_to_write = []
                    for t in all_t_index.values():
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
                print("-"*200)
                print(f"The task has been reassigned to {reassign_user}.")
        else:
            print("-"*200)
            print("This username does not exist on the system.", end = " ")
            print("(Note: input is case and space sensitive)")
            print("No task was reassigned")


def vm_change_date(t_choice, index_dict, all_t_index):
    '''Allows the user to enter a new due date they want to assign to a task.
    Consequently, if said new due date changes how an overdue task is now
    not overdue this change will be reflected both in the console and tasks.txt
    from this point in time and onwards. After the task due date is changed
    the user is notified of this and returned to view all tasks assigned to
    them on the system.

    Conditions required for changing task due date:
        - The task is marked as incomplete.
        - The given due date has not already passed.
        - The given due date is different from the due date already assigned
          to the task.

    While the chosen task is marked as complete the due date of a task can't be
    changed. Therefore, before changing the due date of the task the user or
    the user currently assigned to the task must mark the task as incomplete.
    
    If any of the above criteria are not met the user is notified this and
    returned to view all tasks assigned to them on the system.

            Parameters:
                    t_choice (int): A number matching a key in index_dict.

                    index_dict (dict): Dictionary matching an index number of
                        user-specific tasks in tasks.txt to an index number of
                        all tasks in tasks.txt.

                    all_t_index (dict): Dictionary matching an index number
                        to a task in tasks.txt.
                        A task is a dictionary of task components.
    '''
    if all_t_index[index_dict[t_choice]]['completed']:
        print("-"*200)
        print("The due date of a task can not be changed", end = " ")
        print("if the task has been marked as complete.")
    else:
        print("-"*200)
        print("CHANGE DUE DATE")
        while True:
            try:
                print("-"*200)
                new_date =  input('''Please enter the new due date of the task\
 (YYYY-MM-DD,hh:mm):\n''')
                new_date = dt.strptime(new_date, DT_FORMAT)       
                if new_date == all_t_index[index_dict[t_choice]]['due_date']:
                    print("-"*200)
                    print("The task due date is already", end = " ")
                    print(f"{new_date.strftime(DT_FORMAT)}.")
                    break
                elif new_date < dt.now():
                    print("-"*200)
                    print("You are unable to assign a due date", end = " ")
                    print("that has already passed.")
                    break
                else:
                    # Change 'due_date' and 'overdue' status of the task.
                    for index, t in all_t_index.items():
                        if index == index_dict[t_choice]:
                            t['due_date'] = new_date
                            t['overdue'] = True if new_date < dt.now() else False
                    with open("tasks.txt", "w") as task_file:
                        task_list_to_write = []
                        for t in all_t_index.values():
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
                    print("-"*200)
                    print("The task due date has been changed to", end = " ")
                    print(f"{new_date.strftime(DT_FORMAT)}.")
                    break
            except ValueError:
                print("-"*200)
                print("Invalid date format.", end = " ")
                print("Please use the format specified.")
            break


def generate_report():
    '''This feature can only be accessed by the admin user.
    Reads and rewrites tasks.txt in case the overdue status of a task changes.
    But primarily, reads information from task.txt and users.txt to generate:
        - task_overview.txt (summarising task statistics)
        - user_overview.txt (summarising user statistics)

    After the admin is notified via the console that the summary files have
    been generated the admin is returned to the main menu.
    
    task_overview.txt displays:
        - The total number of task
        - The number of completed tasks
        - The number of incomplete and overdue tasks
        - The percentage of incomplete tasks
        - The percentage of overdue tasks
    
    user_overview.txt displays:
        - The number of users
        - The number of tasks generated and tracked
        - The following information per user:
            - Username
            - Number of tasks
            - Percentage of all tasks assigned to this user
            - Percentage of tasks completed
            - Percentage of tasks incomplete
            - Percentage of tasks incomplete and overdue

    To avoid the case of an empty tasks.txt file and subsequent calculations
    raising a ZeroDivisionError, preset overview outputs of task_overview.txt
    and user_overview.txt will be written.
    '''
    with open("users.txt", "r") as user_file:
        user_data = user_file.read().split("\n")

    username_password = {}
    for user in user_data:
        username, password = user.split(";")
        username_password[username] = password

    with open("tasks.txt", "r") as task_file:
        task_data = task_file.read().split("\n")
        task_data = [t for t in task_data if t != ""]

    task_list = []
    for task_string in task_data:
        curr_t = {}
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

    if not task_list:
        t_oview = "TASK OVERVIEW\n"
        t_oview += "-------------------------------------------------------\n"
        t_oview += "Number of tasks:                                 0\n"
        t_oview += "Number of completed tasks:                      N/A\n"
        t_oview += "Number of incomplete and overdue tasks:         N/A\n"
        t_oview += "Percentage of incomplete tasks:                 N/A\n"
        t_oview += "Percentage of overdue tasks:                    N/A\n"
        t_oview += "-------------------------------------------------------\n"
    else:
        num_tasks = len(task_list)

        complete_t_list = [t for t in task_list if t['completed']]
        num_complete_t = len(complete_t_list)

        num_incomplete_t = num_tasks - num_complete_t
        per_incomplete = format((num_incomplete_t/num_tasks)*100,".0f")

        overdue_t_list = [t for t in task_list if t['overdue']]
        num_overdue_t = len(overdue_t_list)
        per_overdue = format((num_overdue_t/num_tasks)*100,".0f")
        # Tasks marked as incomplete and overdue are considered late.
        late_task = []
        for t in task_list:
            if not t['completed'] and t['overdue']:
                late_task.append(t)
        num_late_t = len(late_task)

        t_oview = "TASK OVERVIEW\n"
        t_oview += "-------------------------------------------------------\n"
        t_oview += f"Number of tasks:{" "*32}{num_tasks}\n"
        t_oview += f"Number of completed tasks:{" "*22}{num_complete_t}\n"
        t_oview += f"Number of incomplete and overdue tasks:{" "*9}{num_late_t}\n"
        t_oview += f"Percentage of incomplete tasks:{" "*17}{per_incomplete}%\n"
        t_oview += f"Percentage of overdue tasks:{" "*20}{per_overdue}%\n"
        t_oview += "-------------------------------------------------------"
    with open("task_overview.txt", "w") as t_oview_file:
        t_oview_file.write(t_oview)

    num_users = len(username_password)
    num_tasks = len(task_list)
    u_oview = "USER OVERVIEW\n"
    u_oview += "-------------------------------------------------------\n"
    u_oview += f"Number of users:{" "*32}{num_users}\n"
    u_oview += f"Number of tasks generated and tracked:{" "*10}{num_tasks}\n"
    u_oview += "-------------------------------------------------------\n"

    for user in username_password:
        user_t_list = []
        for t in task_list:
            if t['username'] == user:
                user_t_list.append(t)
        if not user_t_list:
            u_oview += f"{user.capitalize()}\n"
            u_oview += "-------------------------------------------------------\n"
            u_oview += "Number of tasks:                                 0\n"
            u_oview += "Percentage of all tasks assigned to this user:  N/A\n"
            u_oview += "Percentage of tasks completed:                  N/A\n"
            u_oview += "Percentage of tasks incomplete:                 N/A\n"
            u_oview += "Percentage of tasks incomplete and overdue:     N/A\n"
            u_oview += "-------------------------------------------------------\n"
        else:
            u_num_tasks = len(user_t_list)

            u_per_t = format((u_num_tasks/num_tasks)*100,".0f")

            u_complete_t_list = [t for t in user_t_list if t['completed']]
            u_num_complete = len(u_complete_t_list)
            u_per_complete = format((u_num_complete/u_num_tasks)*100,".0f")

            u_num_incomplete_t = u_num_tasks - u_num_complete
            u_per_incomplete = format((u_num_incomplete_t/u_num_tasks)*100,".0f")

            u_late_task = []
            for t in user_t_list:
                if not t['completed'] and t['overdue']:
                    u_late_task.append(t)
            u_num_late_t = len(u_late_task)
            u_per_late = format((u_num_late_t/u_num_tasks)*100,".0f")

            u_oview += f"{user.capitalize()}\n"
            u_oview += "-------------------------------------------------------\n"
            u_oview += f"Number of tasks:{" "*32}{u_num_tasks}\n"
            u_oview += f"Percentage of all tasks assigned to this user:{" "*2}{u_per_t}%\n"
            u_oview += f"Percentage of tasks completed:{" "*18}{u_per_complete}%\n"
            u_oview += f"Percentage of tasks incomplete:{" "*17}{u_per_incomplete}%\n"
            u_oview += f"Percentage of tasks incomplete and overdue:{" "*5}{u_per_late}%\n"
            u_oview += "-------------------------------------------------------\n"
    with open("user_overview.txt", "w") as u_oview_file:
        u_oview_file.write(u_oview)
        print("-"*200)
        print('''The 'task_overview.txt' and 'user_overview.txt' files have\
 been generated/updated.''')


def disp_stats():
    '''This feature can only be accessed by the admin user.
    Reads and rewrites tasks.txt in case the overdue status of a task changes.
    But primarily, reads information from task.txt and users.txt to display
    task overview and user overview statistics to the console.
    Once the statistics have been displayed the admin is returned to the main
    menu.
    
    Task overview statistics displayed:
        - The total number of task
        - The number of completed tasks
        - The number of incomplete and overdue tasks
        - The percentage of incomplete tasks
        - The percentage of overdue tasks
    
    User overview statistics displayed:
        - The number of users
        - The number of tasks generated and tracked
        - The following information per user:
            - Username
            - Number of tasks
            - Percentage of all tasks assigned to this user
            - Percentage of tasks completed
            - Percentage of tasks incomplete
            - Percentage of tasks incomplete and overdue

    To avoid the case of an empty tasks.txt file and subsequent calculations
    raising a ZeroDivisionError, preset overview outputs will be written
    into the console.
    '''
    with open("users.txt", "r") as user_file:
        user_data = user_file.read().split("\n")

    username_password = {}
    for user in user_data:
        username, password = user.split(";")
        username_password[username] = password

    with open("tasks.txt", "r") as task_file:
        task_data = task_file.read().split("\n")
        task_data = [t for t in task_data if t != ""]

    task_list = []
    for task_string in task_data:
        curr_t = {}
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

    print("="*200)
    print("DISPLAY STATISTICS")
    if not task_list:
        print("-"*200)
        print("TASK OVERVIEW")
        print("-------------------------------------------------------")
        print("Number of tasks:                                 0     ")
        print("Number of completed tasks:                      N/A")
        print("Number of incomplete and overdue tasks:         N/A")
        print("Percentage of incomplete tasks:                 N/A")
        print("Percentage of overdue tasks:                    N/A")
        print("-------------------------------------------------------")
    else:
        num_tasks = len(task_list)

        complete_t_list = [t for t in task_list if t['completed']]
        num_complete_t = len(complete_t_list)

        num_incomplete_t = num_tasks - num_complete_t
        per_incomplete = format((num_incomplete_t/num_tasks)*100,".0f")

        overdue_t_list = [t for t in task_list if t['overdue']]
        num_overdue_t = len(overdue_t_list)
        per_overdue = format((num_overdue_t/num_tasks)*100,".0f")

        late_task = []
        for t in task_list:
            if not t['completed'] and t['overdue']:
                late_task.append(t)
        num_late_t = len(late_task)

        print("-"*200)
        print("TASK OVERVIEW")
        print("-------------------------------------------------------")
        print(f"Number of tasks:{" "*32}{num_tasks}")
        print(f"Number of completed tasks:{" "*22}{num_complete_t}")
        print(f"Number of incomplete and overdue tasks:{" "*9}{num_late_t}")
        print(f"Percentage of incomplete tasks:{" "*17}{per_incomplete}%")
        print(f"Percentage of overdue tasks:{" "*20}{per_overdue}%")
        print("-------------------------------------------------------")

    num_users = len(username_password)
    num_tasks = len(task_list)
    print("USER OVERVIEW")
    print("-------------------------------------------------------")
    print(f"Number of users:{" "*32}{num_users}")
    print(f"Number of tasks generated and tracked:{" "*10}{num_tasks}")
    print("-------------------------------------------------------")

    for user in username_password:
        user_t_list = []
        for t in task_list:
            if t['username'] == user:
                user_t_list.append(t)
        if not user_t_list:
            print(user.capitalize())
            print("-------------------------------------------------------")
            print("Number of tasks:                                 0")
            print("Percentage of all tasks assigned to this user:  N/A")
            print("Percentage of tasks completed:                  N/A")
            print("Percentage of tasks incomplete:                 N/A")
            print("Percentage of tasks incomplete and overdue:     N/A")
            print("-------------------------------------------------------")
        else:
            u_num_tasks = len(user_t_list)

            u_per_t = format((u_num_tasks/num_tasks)*100,".0f")

            u_complete_t_list = [t for t in user_t_list if t['completed']]
            u_num_complete = len(u_complete_t_list)
            u_per_complete = format((u_num_complete/u_num_tasks)*100,".0f")

            u_num_incomplete_t = u_num_tasks - u_num_complete
            u_per_incomplete = format((u_num_incomplete_t/u_num_tasks)*100,".0f")

            u_late_task = []
            for t in user_t_list:
                if not t['completed'] and t['overdue']:
                    u_late_task.append(t)
            u_num_late_t = len(u_late_task)
            u_per_late = format((u_num_late_t/u_num_tasks)*100,".0f")

            print(user.capitalize())
            print("-------------------------------------------------------")
            print(f"Number of tasks:{" "*32}{u_num_tasks}")
            print(f"Percentage of all tasks assigned to this user:{" "*2}{u_per_t}%")
            print(f"Percentage of tasks completed:{" "*18}{u_per_complete}%")
            print(f"Percentage of tasks incomplete:{" "*17}{u_per_incomplete}%")         
            print(f"Percentage of tasks incomplete and overdue:{" "*5}{u_per_late}%")
            print("-------------------------------------------------------")


def edit_profile(current_user, current_pass):
    '''Presents the user with options to change their login details. 

    Non-admin users can:
        - Change their username.
        - Change their password.
        - Return to the main menu.

    The admin can:
        - Change their password.
        - Return to the main menu.
    '''
    print("="*200)
    print("CHANGE LOGIN DETAILS")
    while True:
        edit_choice = ""
        while edit_choice != "r":
            if current_user != "admin":
                edit_choice = input(f'''{"-" * 200}\nWhat do you want to change?
Select one of the following options below:
u - Change my username
p - Change my password
r - Return to the main menu
Enter a letter: ''').lower()
            else:
                edit_choice = input(f'''{"-" * 200}\nWhat do you want to change?
Select one of the following options below:
p - Change my password
r - Return to the main menu
Enter a letter: ''').lower()
            if current_user != "admin" and edit_choice == "u":
                edit_name(current_user, current_pass)
            elif edit_choice == "p":
                edit_pass(current_user)
            elif edit_choice == "r":
                break
            else:
                print("-"*200)
                print("You must enter letter/s from the menu.", end = " ")
                print("(Note: choice input is space sensitive)")
        print("-"*200)
        print("Returning you to the main menu.")
        break


def edit_name(current_user, current_pass):
    '''Reads users.txt to recognise the existing list of users.
    Reads tasks.txt to recognise the existing list of tasks.
    But primarily, allows non-admin users to change their username stored in
    users.txt and activate any corresponding changes in tasks.txt. 
    
    Prompts the user for the following:
        - A new username.
        - Username confirmation.

    Conditions required for username change:
        - The new username mustn't be the same as the current username.
        - The new username mustn't already exists in the users.txt file.
        - The new username and confirmed username must match.
        - The new username can't exceed 163 characters or include ';'.
    
    If any of the above criteria are not met the user is notified this and
    returned to the change login details menu.

    If the above criteria are met, the new username replaces the old username
    stored in users.txt. as "new_username;password" on the same line as before.
    Any tasks in tasks.txt assigned to the current user will now reflect the
    username change and be assigned to the new username.

    The user is notified that their username has been changed and that the
    program will close. A program restart is required for the program to
    function as normal with the new user credentials.
    '''
    with open("users.txt", "r") as user_file:
        user_data = user_file.read().split("\n")

    username_password = {}
    for user in user_data:
        username, password = user.split(";")
        username_password[username] = password

    with open("tasks.txt", "r") as task_file:
        task_data = task_file.read().split("\n")
        task_data = [t for t in task_data if t != ""]

    task_list = []
    for task_string in task_data:
        curr_t = {}
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

    print("-"*200)
    print("USERNAME CHANGE")
    print("-"*200)
    print(f"Your current username is {current_user}.")
    desired_name = input("New username: ")
    confirm_name = input("Confirm new username: ")
    if desired_name in username_password:
        print("-"*200)
        print("This username is taken.", end = " ")
        print("(Note: usernames must be unique)")
        print("No username was changed.")
    elif semicolon_found(desired_name):
        print("No username was changed.")
    elif desired_name != confirm_name:
        print("-"*200)
        print("Your usernames do no match.", end = " ")
        print("(Note: login is case and space sensitive)")
        print("No username was changed.")
    elif character_exceed(desired_name):
        print("No username was changed.")
    else:
        # If valid replace the user's username in users.txt file.
        username_password[desired_name] = current_pass
        with open("users.txt", "w") as user_file:
            user_data = []
            for key in username_password:
                if key != current_user:
                    user_data.append(f"{key};{username_password[key]}")
            user_file.write("\n".join(user_data))
            # Replace instances of the old username in t_comp[0] in tasks.txt.
            for t in task_list:
                if t['username'] == current_user:
                    t['username'] = desired_name    
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
            print("-"*200)
            print(f"Your username has been changed to '{desired_name}'.")
            print("Your password has not been changed.")
            print("This program will now close.")
            print("-"*200)
            print(f"Goodbye {desired_name.capitalize()}!")
            print("-"*200)
            exit()


def edit_pass(current_user):
    '''Reads users.txt to recognise the existing list of users.
    But primarily, allows users to change their password stored in users.txt. 
    
    Prompts the user for the following:
        - A new password.
        - Password confirmation.

    Conditions required for password change:
        - The new password mustn't be the same as the current password.
        - The new password and confirmed password must match.
        - The new password can't exceed 163 characters or include ';'.
    
    If any of the above criteria are not met the user is notified this and
    returned to the change login details menu.

    If the above criteria are met, the new password replaces the old username
    stored in users.txt. as "username;new_password" on the same line as before.

    The user is notified that their password has been changed and that the
    program will close. A program restart is required for the program to
    function as normal with the new user credentials.
    '''
    with open("users.txt", "r") as user_file:
        user_data = user_file.read().split("\n")

    username_password = {}
    for user in user_data:
        username, password = user.split(";")
        username_password[username] = password

    print("-"*200)
    print("PASSWORD CHANGE")
    print("-"*200)
    print(f"Your current password is '{username_password[current_user]}'.")
    desired_pass = input("New password: ")
    confirm_pass = input("Confirm new password: ")
    if desired_pass == username_password[current_user]:
        print("-"*200)
        print("What you typed is identical to your current password.")
        print("No change to your password was made.")
    elif semicolon_found(desired_pass):
        print("No change to your password was made.")
    elif desired_pass != confirm_pass:
        print("-"*200)
        print("Your passwords do no match.", end = " ")
        print("(Note: login is case and space sensitive)")
        print("No change to your password was made.")
    elif character_exceed(desired_pass):
        print("No change to your password was made.")
    else:
        # If valid replace the user's password in users.txt file.
        username_password[current_user] = desired_pass
        with open("users.txt", "w") as user_file:
            user_data = []
            for key in username_password:
                user_data.append(f"{key};{username_password[key]}")
            user_file.write("\n".join(user_data))
        print("-"*200)
        print(f"Your password has been changed to '{desired_pass}'.")
        print("This program will now close.")
        print("-"*200)
        print(f"Goodbye {current_user.capitalize()}!")
        print("-"*200)
        exit()
