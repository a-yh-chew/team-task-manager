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

## Installation

Install the team-task-manager package with pip

```
pip install team-task-manager
```
## How it works
#### When the script (*team_task_manager.py*) is initiated the following files are generated:
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

If you find a bug, have ideas for new features, other improvements, or require more clarity on the project please submit an [issue](https://github.com/a-yh-chew/team-task-manager/issues).



## Author

Angela Chew (GitHub: [a-yh-chew](https://github.com/a-yh-chew), e-mail: a.yh.chew@gmail.com)


## License

[Apache 2.0 License](https://www.apache.org/licenses/LICENSE-2.0.txt.)
