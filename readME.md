# ![milvus_icon.png](images%2Fmilvus_icon.png) Milvus **R**ole **B**ase **A**ccess **C**ontrol
## Users: 
Milvus creates a root user by default with a default password Milvus. The root user is 
granted the admin privileges, which means that this root user can have access to all 
resources and perform all actions.
### Current Situation:
Only `root` user is there and no role is implemented. APIs access through `root` user.
### What is users, roles, objects, and privileges in role-based access control (RBAC).
* **Object:** An object to grant or deny access to. The object can be a collection, a partition, etc.
* **User:** A user identity with a username and a corresponding password.
* **Privilege:** A privilege defines the actions that can be performed and resources that can be accessed. A privilege cannot be granted to a user directly. It has to be granted to a role first.
* **Role:** A role defines the privilege(s) a user has to certain objects. After binding a role to a user, the user inherits all the privileges that are granted to this role.
## Proposed RBAC Architecture:
![rbac_architecture.png](images%2Frbac_architecture.png)
### Files in this repository
#### [config.ini](config%2Fconfig.ini)
Place your configuration here. <br>
**MILVUS** section is used to mention your Milvus database connection credentials.<br>
**LOG** section is used to mention the logging configuration.<br>
You can mention `n`  number of teams as per your need, the format should be same!<br>
TEAM_`n` <br>
team`n`_user_name = my_team1_usr <br>
team`n`_passwd = passw0rd <br>
team`n`_role_name = my_team1_role <br>
You can mention multiple collections as comma separated string. <br>
team`n`_collections = Album1, SongAlbum <br>

#### [create_rbac.py](create_rbac.py)
The main file which implements Role Base Access Control (RBAC). Run `python .\create_rbac.py`
#### [test_rbac.py](test_rbac.py) 
For unit testing. Run `python -m unittest -v`
#### [delete_role_user.py](delete_role_user.py)
Used for deleting Role and User. Run `python .\delete_role_user.py`