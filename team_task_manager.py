#==========Language Notes==========
# The use of "t" in this document is short for "task".
# 'u' is short for 'user'.
# "curr" is short for "current".
# "dt" is short for "datetime".
# "vm" is short for "view my".
# 'disp' is short for 'display'.
# 'oview' is short for 'overview'.
# 'per' is short for 'percent'.

#==========Importing Libraries==========
import os
from datetime import datetime as dt
import math  # Enabling the use of 'math.floor'.

#=====Constant Variables=====
# This is our chosen date format.
DT_FORMAT = "%Y-%m-%d,%H:%M"

#==========Functions==========
def semicolon_found(*args):  
# This function checks if the input includes semicolon.
# Semicolons in this program are used to separate 'task_list' elements.
# Semicolons will disrupt the functionality of this program if accepted.
    if ";" in args:
        print("-" * 200)
        print("Your entry is invalid.", end = " ")
        print("(Note: please do not enter inputs containing ';')")
        return True
    else:
        return False
    
def character_exceed(*args):
# The 182 character limit is for the sake of presentation.
# To stay within the 200 character length border lines.
    if len(args) > 182:
        print("-" * 200)
        print("Input length was too long.", end = " ")
        print("(Note: input should be 182 characters maximum)")
        return True
    else:
        return False
    

def reg_user():  # Adds a new user to the 'user.txt' file.
    print("=" * 200)
    print("REGISTERING A USER")
    print("-" * 200)
    # Request input of a new username, password, and password confirmation. 
    new_username = input("New Username: ")
    new_password = input("New Password: ")
    confirm_password = input("Confirm Password: ")
    # Check if the new username already exists in our dictionary.
    if new_username in username_password:
        print("-" * 200)
        print("This username is taken.", end = " ")
        print("(Note: usernames must be unique)")
        print("No new user was added.")
    elif semicolon_found(new_username, new_password):
        print("No new user was added.")
    # Check if the new password and confirmed password match.
    elif new_password != confirm_password:
        print("-" * 200)
        print("Passwords do no match.", end = " ")
        print("(Note: login is case and space sensitive)")
        print("No new user was added.")
    elif character_exceed(new_username, new_password):
        print("No new user was added.")
    else:
        # If passwords match, add the new user into user.txt file.
        username_password[new_username] = new_password
        with open("user.txt", "w") as reg_file:
            user_data = []
            for key in username_password:
                user_data.append(f"{key};{username_password[key]}")
            reg_file.write("\n".join(user_data))
        print("-" * 200)
        print(f"New user '{new_username}' was added.")
        

def add_task():  # Adds a new task to the 'tasks.txt' file.
    print("=" * 200)
    print("ADDING A TASK")
    print("-" * 200)
    ''' Prompt a user for the following: 
            - A username of the person whom the task is assigned to,
            - A title of a task,
            - A description of the task
            - The due date of the task.'''
    task_username = input("Username of the person assigned this task: ")
    if task_username not in username_password:
        print("-" * 200)
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
                        if task_due_date > dt.now():
                            break
                        else:
                            print("-" * 200)
                            print("You are unable to assign a ", end = " ")
                            print("due date that has already passed.")
                            print("-" * 200)
                    except ValueError:
                        print("-" * 200)
                        print("Invalid date format.", end = " ")
                        print("Please use the format specified.")
                        print("-" * 200)

                ''' Add the data to the file task.txt and
                    Include 'No' to indicate if the task is complete.
                    Include an indication of whether the task is overdue'''
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
                print("-" * 200)
                print(task_username.capitalize(), end =" ")
                '''Feedback to user:
                    -The user that has been given the new task.
                    -The dt set.
                    -The dt due.
                    -The time(days and hours) given to complete the task.'''
                print(f"has been assigned a new task.")
                print(f"Set on: {dt.now().strftime(DT_FORMAT)}.")
                print(f"Due by: {task_due_date.strftime(DT_FORMAT)}.")
                # Calculate and format the time given to complete the task.
                time_diff = task_due_date - dt.now()
                seconds = time_diff.total_seconds()
                days = divmod(seconds, 86400)
                hours = divmod(days[1], 3600)
                print(f'''Approximate time given to complete the task: 
{math.floor(days[0])} Days and {math.floor(hours[0])} hours.''')
                

def view_all_tasks():
# Read and rewrite tasks.txt keeping the user presented info up to date.
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
    # Read and print all tasks from task.txt to the console.
    # Ask which task the user wants to manage (via index).
    # Or they can return to the menu (via entering '-1').
    while True:
        t_choice = ""
        while t_choice != -1:
            try:
                print("=" * 200)
                print("VIEW ALL TASKS")
                all_t_index = {}
                for index, t in enumerate(task_list, start = 1):
                    all_t_index[index] = t
                    print("-" * 200)  # Capitalise the strings displayed.
                    disp = f"Task number:\t  {index}\n"
                    disp += f"Task:\t\t  {t['title'].capitalize()}\n"
                    disp += f"Task Description: {t['description'].capitalize()}\n"
                    disp += f"Assigned to:\t  {t['username'].capitalize()}\n"
                    disp += f"Date Assigned:\t  {t['assigned_date'].strftime(DT_FORMAT)}\n"
                    disp += f"Due Date: \t  {t['due_date'].strftime(DT_FORMAT)}\n"
                    disp += f"Completed:\t  {'Yes' if t['completed'] else 'No'}\n"
                    disp += f"Overdue:\t  {'Yes' if t['overdue'] else 'No'}"
                    print(disp)
                print("-" * 200)
                print(f"There are a total of {len(task_list)} tasks.")
                # If the user isn't the admin return to menu.
                if current_user != "admin":
                    break
                # If there's no tasks return to menu.
                elif len(task_list) == 0:
                    break
                else:
                    print("-" * 200)  # Must cast vm_t_choice as an integer.
                    t_choice =  int(input('''Please enter the number of the \
task you would like to manage (or enter '-1' to return to the main menu): '''))       
                    # Only if 't_choice' is within the index of tasks.
                    # The user proceeds to the task management options.
                    if t_choice in all_t_index:
                        manage_t(t_choice, all_t_index)
                    elif t_choice == -1:
                        break
                    else:
                        print("-" * 200)
                        print("You must enter a valid number.")
            except ValueError:  # Error handling for non integer t_choice.
                print("-" * 200)
                print("You must enter a valid whole number.")
        print("-" * 200)
        print("Returning you to the main menu.")
        break


def manage_t(t_choice, all_t_index):  
# Admin chooses what about the chosen task they want to manage.
    t = all_t_index.get(t_choice)
    print("=" * 200)
    print("MANAGE TASK")
    while True:
        manage_choice = ""
        while manage_choice != "v":
            print("-" * 200)  # Display the task the user has selected.
            print("You have chosen to manage the task below:")
            print("-" * 200)
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
                print("-" * 200)
                print("You must enter a letter from the menu.", end = " ")
                print("(Note: choice input is space sensitive)")
        print("-" * 200)
        print("Returning to view the other tasks.")
        break        


def mark_complete(t_choice, all_t_index):
# Asks admin to enter 'c' to change the completion status of the task.
# Or enter 'r' to leave this function.
    print("-" * 200)
    print("CHANGE COMPLETION STATUS")
    while True:
        mark_choice = ""
        while mark_choice != "r":
            print("-" * 200)
            mark_choice =  input('''Please enter 'c' to change the completion\
 status of the task (changing 'Yes' to 'No', or changing 'No' to 'Yes') (or\
 enter 'r' to return to the task managing options):\n''').lower()
            if mark_choice == "c":
                # Switch 'completed' status of the chosen task.
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
                print("-" * 200)
                print("The completion status of the task has been changed.")
                break
            elif mark_choice == "r":
                break
            else:
                print("-" * 200)
                print("You must enter a valid letter.", end = " ")
                print("(Note: choice input is space sensitive)")
        break


def change_person(t_choice, all_t_index):
# Allows admin to change the user the task is assigned to.
# Unless the task is already marked as completed.
    if all_t_index[t_choice]['completed']:
        print("-" * 200)
        print("The user assigned to a task can not be changed", end = " ")
        print("if the task has been marked as complete.")
    else:
        print("-" * 200)
        print("REASSIGN TASK")
        print("-" * 200)
        reassign_user =  input('''Please enter the username of the user\
 you want to reassign the task to:\n''')
        if reassign_user in username_password:
            if reassign_user == all_t_index[t_choice]['username']:
                print("-" * 200)
                print(f"The task is already assigned to {reassign_user}.")
            else:
                # Switch 'username' of the chosen task.
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
                print("-" * 200)
                print(f"The task has been reassigned to {reassign_user}.")
        else:
            print("-" * 200)
            print("This username does not exist on the system.", end = " ")
            print("(Note: input is case and space sensitive)")
            print("No task was reassigned")


def change_date(t_choice, all_t_index):
# Allows admin to change the due date of the task.
# Unless the task is already marked as completed.
    if all_t_index[t_choice]['completed']:
        print("-" * 200)
        print("The due date of a task can not be changed", end = " ")
        print("if the task has been marked as complete.")
    else:
        print("-" * 200)
        print("CHANGE DUE DATE")
        while True:
            try:
                print("-" * 200)
                new_date =  input('''Please enter the new due date of the task\
 (YYYY-MM-DD,hh:mm):\n''')
                new_date = dt.strptime(new_date, DT_FORMAT)       
                if new_date == all_t_index[t_choice]['due_date']:
                    print("-" * 200)
                    print("The task due date is already", end = " ")
                    print(f"{new_date.strftime(DT_FORMAT)}.")
                    break
                elif new_date < dt.now():
                    print("-" * 200)
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
                    print("-" * 200)
                    print("The task due date has been changed to", end = " ")
                    print(f"{new_date.strftime(DT_FORMAT)}.")
                    break
            except ValueError:
                print("-" * 200)
                print("Invalid date format.", end = " ")
                print("Please use the format specified.")
            break


def view_my_tasks():
    # Read and rewrite tasks.txt keeping the user presented data up to date.
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
    # Read and print the current user's tasks from task.txt to the console.
    # Ask which task the user wants to manage (via index).
    # Or they can return to the menu (via entering '-1').
    while True:
        t_choice = ""
        while t_choice != -1:
            try:
                print("=" * 200)
                print("VIEW MY TASKS")
                # Enumerate through all_t_index to index user-specific tasks.
                # Enumerate through task_list to index all tasks.
                # Make dictionary of 'user-specific index' to 'overall index'.
                all_t_index = {}
                my_index = 0
                index_dict = {}
                for index, t in enumerate(task_list, start = 1):
                    all_t_index[index] = t
                    if t['username'] == current_user:
                        my_index += 1
                        index_dict[my_index] = index
                        print("-" * 200)
                        disp = f"Task number:\t  {my_index}\n"
                        disp += f"Task:\t\t  {t['title'].capitalize()}\n"
                        disp += f"Task Description: {t['description'].capitalize()}\n"
                        disp += f"Assigned to:\t  {t['username'].capitalize()}\n"
                        disp += f"Date Assigned:\t  {t['assigned_date'].strftime(DT_FORMAT)}\n"
                        disp += f"Due Date: \t  {t['due_date'].strftime(DT_FORMAT)}\n"
                        disp += f"Completed:\t  {'Yes' if t['completed'] else 'No'}\n"
                        disp += f"Overdue:\t  {'Yes' if t['overdue'] else 'No'}"
                        print(disp)
                print("-" * 200)
                print(f"There are a total of {my_index} tasks for you.")
                # If there's no tasks return to menu.
                if my_index == 0:
                    break
                else:
                    print("-" * 200)
                    t_choice =  int(input('''Please enter the number of the\
 task you would like to manage or enter '-1' to return to the main menu:\n'''))       
                    if t_choice in index_dict:
                        vm_manage_t(t_choice,index_dict, all_t_index)
                    elif t_choice == -1:
                        break
                    else:
                        print("-" * 200)
                        print("You must enter a valid number.")
            except ValueError:
                print("-" * 200)
                print("You must enter a valid whole number.")
        print("-" * 200)
        print("Returning you to the main menu.")
        break


def vm_manage_t(t_choice,index_dict, all_t_index):
# User chooses what about the chosen task they want to manage.
    t = all_t_index.get(index_dict[t_choice])
    print("=" * 200)
    print("MANAGE TASK")
    while True:
        manage_choice = ""
        while manage_choice != "v":
            print("-" * 200)  # Display the task the user has selected.
            print("You have chosen to manage the task below:")
            print("-" * 200)
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
                print("-" * 200)
                print("You must enter a letter from the menu.", end = " ")
                print("(Note: choice input is space sensitive)")
        print("-" * 200)
        print("Returning to view the other tasks.")
        break        


def vm_mark_complete(t_choice,index_dict, all_t_index):
# Asks user to enter 'c' to change the completion status of the task.
# Or enter 'r' to leave this function.
    print("-" * 200)
    print("CHANGE COMPLETION STATUS")
    while True:
        mark_choice = ""
        while mark_choice != "r":
            print("-" * 200)
            mark_choice =  input('''Please enter 'c' to change the completion\
 status of the task (changing 'Yes' to 'No', or changing 'No' to 'Yes') (or\
 enter 'r' to return to the task managing options):\n''').lower()
            if mark_choice == "c":
                # Switch 'completed' status of the chosen task.
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
                print("-" * 200)
                print("The completion status of the task has been changed.")
                break
            elif mark_choice == "r":
                break
            else:
                print("-" * 200)
                print("You must enter a valid letter.", end = " ")
                print("(Note: choice input is space sensitive)")
        break


def vm_change_person(t_choice, index_dict, all_t_index):
# Allows user to change the user the task is assigned to.
# Unless the task is already marked as completed.
    if all_t_index[index_dict[t_choice]]['completed']:
        print("-" * 200)
        print("The user assigned to a task can not be changed", end = " ")
        print("if the task has been marked as complete.")
    else:
        print("-" * 200)
        print("REASSIGN TASK")
        print("-" * 200)
        reassign_user =  input('''Please enter the username of the user\
 you want to reassign the task to:\n''')
        if reassign_user in username_password:
            if reassign_user == all_t_index[index_dict[t_choice]]['username']:
                print("-" * 200)
                print(f"The task is already assigned to {reassign_user}.")
            else:
                # Switch 'username' of the chosen task.
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
                print("-" * 200)
                print(f"The task has been reassigned to {reassign_user}.")
        else:
            print("-" * 200)
            print("This username does not exist on the system.", end = " ")
            print("(Note: input is case and space sensitive)")
            print("No task was reassigned")


def vm_change_date(t_choice, index_dict, all_t_index):
# Allows user to change the due date of the task.
# Unless the task is already marked as completed.
    if all_t_index[index_dict[t_choice]]['completed']:
        print("-" * 200)
        print("The due date of a task can not be changed", end = " ")
        print("if the task has been marked as complete.")
    else:
        print("-" * 200)
        print("CHANGE DUE DATE")
        while True:
            try:
                print("-" * 200)
                new_date =  input('''Please enter the new due date of the task\
 (YYYY-MM-DD,hh:mm):\n''')
                new_date = dt.strptime(new_date, DT_FORMAT)       
                if new_date == all_t_index[index_dict[t_choice]]['due_date']:
                    print("-" * 200)
                    print("The task due date is already", end = " ")
                    print(f"{new_date.strftime(DT_FORMAT)}.")
                    break
                elif new_date < dt.now():
                    print("-" * 200)
                    print("You are unable to assign a due date", end = " ")
                    print("that has already passed.")
                    break
                else:
                    # Chnage 'due_date' and 'overdue' status of the task.
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
                    print("-" * 200)
                    print("The task due date has been changed to", end = " ")
                    print(f"{new_date.strftime(DT_FORMAT)}.")
                    break
            except ValueError:
                print("-" * 200)
                print("Invalid date format.", end = " ")
                print("Please use the format specified.")
            break


def generate_report():
# Read/write tasks.txt to update the 'overdue' status if there's any change.
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
    # What's written into 'task_overview.txt' if 'tasks.txt' is empty.
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
        per_incomplete = format((num_incomplete_t/num_tasks)*100,".1f") 

        overdue_t_list = [t for t in task_list if t['overdue']]
        num_overdue_t = len(overdue_t_list)
        per_overdue = format((num_overdue_t/num_tasks)*100,".1f") 
        # Tasks marked as incomplete and overdue are considered late.
        late_task = []
        for t in task_list:
            if not t['completed'] and t['overdue']:
                late_task.append(t)
        num_late_t = len(late_task)
        # What's written into 'task_overview.txt' if 'tasks.txt' isn't empty.
        t_oview = "TASK OVERVIEW\n"
        t_oview += "-------------------------------------------------------\n"
        t_oview += f"Number of tasks:{" "*32}{num_tasks}\n"
        t_oview += f"Number of completed tasks:{" "*22}{num_complete_t}\n"
        t_oview += f"Number of incomplete and overdue tasks:{" "*9}{num_late_t}\n"
        t_oview += f"Percentage of incomplete tasks:{" "*17}{per_incomplete}%\n"
        t_oview += f"Percentage of overdue tasks:{" "*20}{per_overdue}%\n"
        t_oview += "-------------------------------------------------------"
    # Writing/rewriting 't_oview' into the 'task_overview.txt' file.
    with open("task_overview.txt", "w") as t_oview_file:
        t_oview_file.write(t_oview)

    num_users = len(username_password)
    num_tasks = len(task_list)
    # Written into 'user_overview.txt'.
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
        # What's written into 'user_overview.txt' if a user has no tasks.
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

            u_per_t = format((u_num_tasks/num_tasks)*100,".1f")

            u_complete_t_list = [t for t in user_t_list if t['completed']]
            u_num_complete = len(u_complete_t_list)
            u_per_complete = format((u_num_complete/u_num_tasks)*100,".1f") 

            u_num_incomplete_t = u_num_tasks - u_num_complete
            u_per_incomplete = format((u_num_incomplete_t/u_num_tasks)*100,".1f") 

            u_late_task = []
            for t in user_t_list:
                if not t['completed'] and t['overdue']:
                    u_late_task.append(t)
            u_num_late_t = len(u_late_task)
            u_per_late = format((u_num_late_t/u_num_tasks)*100,".1f") 
            # What's written into 'user_overview.txt' if a user has tasks.
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
        print("-" * 200)
        print('''The 'task_overview.txt' and 'user_overview.txt' files have\
 been generated/updated.''')


def disp_stats():
    # 'tasks_overview.txt' and 'users_overview.txt' will be generated/updated.
    generate_report()  
    #  Display task and user overview info in console.
    print("=" * 200)
    print("DISPLAY STATISTICS")
    # What's written into the console if 'tasks.txt' is empty.
    if not task_list:
        print("-" * 200)
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
        per_incomplete = format((num_incomplete_t/num_tasks)*100,".1f") 

        overdue_t_list = [t for t in task_list if t['overdue']]
        num_overdue_t = len(overdue_t_list)
        per_overdue = format((num_overdue_t/num_tasks)*100,".1f") 
        
        late_task = []
        for t in task_list:
            if not t['completed'] and t['overdue']:
                late_task.append(t)
        num_late_t = len(late_task)
        # What's written into the console if 'tasks.txt' isn't empty.
        print("-" * 200)
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
        # What's written into the console if a user has no tasks.
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

            u_per_t = format((u_num_tasks/num_tasks)*100,".1f")

            u_complete_t_list = [t for t in user_t_list if t['completed']]
            u_num_complete = len(u_complete_t_list)
            u_per_complete = format((u_num_complete/u_num_tasks)*100,".1f") 

            u_num_incomplete_t = u_num_tasks - u_num_complete
            u_per_incomplete = format((u_num_incomplete_t/u_num_tasks)*100,".1f") 

            u_late_task = []
            for t in user_t_list:
                if not t['completed'] and t['overdue']:
                    u_late_task.append(t)
            u_num_late_t = len(u_late_task)
            u_per_late = format((u_num_late_t/u_num_tasks)*100,".1f") 
            # What's written into the console if a user has tasks.
            print(user.capitalize())
            print("-------------------------------------------------------")
            print(f"Number of tasks:{" "*32}{u_num_tasks}")
            print(f"Percentage of all tasks assigned to this user:{" "*2}{u_per_t}%")
            print(f"Percentage of tasks completed:{" "*18}{u_per_complete}%")
            print(f"Percentage of tasks incomplete:{" "*17}{u_per_incomplete}%")                    
            print(f"Percentage of tasks incomplete and overdue:{" "*5}{u_per_late}%")        
            print("-------------------------------------------------------")


def edit_profile():
# User chooses whether they want to change their username or password.
    print("=" * 200)
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
                edit_name()
            elif edit_choice == "p":
                edit_pass()
            elif edit_choice == "r":
                break
            else:
                print("-" * 200)
                print("You must enter letter/s from the menu.", end = " ")
                print("(Note: choice input is space sensitive)")
        print("-" * 200)
        print("Returning you to the main menu.")
        break        


def edit_name():
# Non-admin users can change their username stored in the 'users.txt' file.
    print("-" * 200)
    print("USERNAME CHANGE")
    print("-" * 200)
    # Request input of a desired username and confirmation.
    print(f"Your current username is {current_user}.")
    desired_name = input("New username: ")
    confirm_name = input("Confirm new username: ")
    # Check if the desired username already exists in our dictionary.
    if desired_name in username_password:
        print("-" * 200)
        print("This username is taken.", end = " ")
        print("(Note: usernames must be unique)")
        print("No username was changed.")
    elif semicolon_found(desired_name):
        print("No username was changed.")
    # Check if the new password and confirmed password match.
    elif desired_name != confirm_name:
        print("-" * 200)
        print("Your usernames do no match.", end = " ")
        print("(Note: login is case and space sensitive)")
        print("No username was changed.")
    elif character_exceed(desired_name):
        print("No username was changed.")
    else:
        # If valid replace the user's username in user.txt file.
        username_password[desired_name] = current_pass
        with open("user.txt", "w") as user_file:
            user_data = []
            for key in username_password:
                if key != current_user:
                    user_data.append(f"{key};{username_password[key]}")
            user_file.write("\n".join(user_data))
            # Replace instances of the old username in t_comp[0].
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
            print("-" * 200)
            print(f"Your username has been changed to '{desired_name}'.")
            print("Your password has not been changed.")
            print("This program will now close.")
            print("-" * 200)
            print(f"Goodbye {desired_name.capitalize()}!")
            print("-" * 200)
            exit()  # Program restart needed to work with the new name.


def edit_pass():
# Users can change their password stored in the 'users.txt' file.
    print("-" * 200)
    print("PASSWORD CHANGE")
    print("-" * 200)
    print(f"Your current password is '{username_password[current_user]}'.")
    # Request input of a desired password and confirmation.
    desired_pass = input("New password: ")
    confirm_pass = input("Confirm new password: ")
    # Check if the desired username already exists in our dictionary.
    if desired_pass == username_password[current_user]:
        print("-" * 200)
        print("What you typed is identical to your current password.")
        print("No change to your password was made.")
    elif semicolon_found(desired_pass):
        print("No change to your password was made.")
    # Check if the new password and confirmed password match.
    elif desired_pass != confirm_pass:
        print("-" * 200)
        print("Your passwords do no match.", end = " ")
        print("(Note: login is case and space sensitive)")
        print("No change to your password was made.")
    elif character_exceed(desired_pass):
        print("No change to your password was made.")
    else:
        # If valid replace the user's password in user.txt file.
        username_password[current_user] = desired_pass
        with open("user.txt", "w") as user_file:
            user_data = []
            for key in username_password:
                user_data.append(f"{key};{username_password[key]}")
            user_file.write("\n".join(user_data))
        print("-" * 200)
        print(f"Your password has been changed to '{desired_pass}'.")
        print("This program will now close.")
        print("-" * 200)
        print(f"Goodbye {current_user.capitalize()}!")
        print("-" * 200)
        exit()  # Program restart required to continue with the new password.

#==========Startup Notes==========
# Use the following username and password to access the admin rights.
# username: admin (this is not changeable).
# password: password (this can be changed after logging in).

#==========Other Notes==========
# If the 'overdue' status of task is incorrect (showing False instead of True).
# This is due to current dt only being counted at the start of the following:
# 'view_all_tasks', 'view_my_tasks', 'generate_reports', and 'disp_stats'.
# The fix to the incorrect status is to re-initialise one of these sections.

#==========Main Structure==========
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

#==========Login Section==========
# Reads usernames and password from the user.txt file to allow a user to login.
# If there's no user.txt file, write one with a default admin account.
if not os.path.exists("user.txt"):
    with open("user.txt", "w") as default_file:
        default_file.write("admin;password")

# Read each line of user.txt as an element in the 'user_data' list.
with open("user.txt", "r") as user_file:
    user_data = user_file.read().split("\n")

# Convert user_data list into a dictionary.
username_password = {}
for user in user_data:
    username, password = user.split(";")
    username_password[username] = password

logged_in = False
while not logged_in:
    print("=" * 200)
    print("LOGIN")
    current_user = input("Username: ")
    current_pass = input("Password: ")
    if current_user not in username_password:
        print("-" * 200)
        print("User does not exist.", end = " ")
        print("(Note: login is case and space sensitive)")
        continue
    elif username_password[current_user] != current_pass:
        print("-" * 200)
        print("Wrong password.", end = " ")
        print("(Note: login is case and space sensitive)")
        continue
    else:
        print("-" * 200)
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
Enter letter/s: ''').lower()  # Input converted to lower case.
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
        reg_user()
    elif choice == "a":
        add_task()
    elif choice == "va":
        view_all_tasks()
    elif choice == "vm":
        view_my_tasks()
    elif current_user == "admin" and choice == "gr":
        generate_report()
    elif current_user == "admin" and choice == "ds":
        disp_stats() 
    elif choice == "c":
        edit_profile()
    elif choice == "e":
        break
    else:
        print("-" * 200)
        print("You must enter letter/s from the menu.", end = " ")
        print("(Note: choice input is space sensitive)")
print("-" * 200)
print(f"Goodbye {current_user.capitalize()}!")
print("-" * 200)
exit()

#==========To be added==========
# Who assigned the task as a task component.
# Who and when last edited the task as a task component.
# Display how much time left to complete the tasks.
# Handling 'IndexError: list index out of range' for anomalies in .txt files. 