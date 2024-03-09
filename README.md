# team-task-manager

This is a simple task management system small businesses can use.


## In this README
- Requirements
- Installation
- How it works
- Contributing
- Author
- License
## Requirements
#### Before you continue, ensure you have met the following requirements:
- Python 3.12 or newer is recommended.
- pip 24.0 or newer is recommended.
- setuptools 69.1.1 or newer is recommended.
- You are using a Windows OS. Linux and Mac OS are not currently supported.

#### Extra requirements:
- pytest 8.0.2 or newer is recommended.
- twine 5.0.0 or newer is recommended.

A full list of the required packages and their respective dependencies can be found in the **requirements.txt** file of this project's [GitHub repository](https://github.com/a-yh-chew/team-task-manager).
## Installation
If you don't have Python installed on your system, see [here](https://wiki.python.org/moin/BeginnersGuide/Download) for instructions of how to do this. Make sure your version of Python is 3.12 or newer.

From Python version 3.4 onwards pip is included by default. With Python and pip you can open a terminal and use pip-commands to install packages.
###
1.  It's recommended to create a virtual environment (see [here](https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/) for instructions of how to do this) to house the team-task-manager package and its package dependencies, though this is optional.
####
2.  Make sure that your environment has all the required packages installed.
####
3.  Next, run the installation syntax presented at the top of [https://pypi.org/project/team-task-manager/](https://pypi.org/project/team-task-manager/) starting with 'pip install'.
####
4.  Once the team-task-manager package and the required packages are installed in your environment, assuming you have followed a process resembling the one [here](https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/), you should be able to locate team_task_manager.py through the path:
~~~
project_directory\.venv\Lib\site-packages\team-task-manager\team_task_manager.py
~~~
####
5.  Open and run team_task_manager.py in your preferred IDE to use the team-task-manager, operated through inputs to the console.

## How it works
#### When team_task_manager.py is run the following files are generated:
- users.txt - Containing user login information.
- tasks.txt - Containing tasks records. 
---
#### After logging in with the default admin credentials:
- username = admin
- password = password  
#### The following features are available to the admin:
  - Registering new users
  - Assigning a new task to a user
  - Viewing and modifying all tasks on the system
  - Viewing and modifying all tasks assigned to the current user (in this case the admin)
  - Generating summary reports as text files
  - Displaying the summary reports in the console
  - Changing login credentials (though the admin can only change their password)
  - Exiting the program
  ---
#### After the admin has registered new users, the following features are available to non-admin users:
  - Registering new users
  - Assigning a new task to a user
  - Viewing all tasks on the system
  - Viewing and modifying all tasks assigned to the current user
  - Changing login credentials
  - Exiting the program
## Contributing

If you find a bug, have ideas for new features, other improvements, or require more clarity on this project please submit an [issue](https://github.com/a-yh-chew/team-task-manager/issues).



## Author

Angela Chew (GitHub: [a-yh-chew](https://github.com/a-yh-chew), E-mail: a.yh.chew@gmail.com)


## License

[MIT](https://choosealicense.com/licenses/mit/)
