from pymilvus import (connections, utility, Role)
import sys
from libs import ReadConfig


def connect_to_milvus(connection_alias):
    try:
        my_config = ReadConfig("config/config.ini")
        # Connecting to my local Milvus in docker image.
        connections.connect(connection_alias,
                            host=str(getattr(my_config, "host")),
                            port=int(getattr(my_config, "port")),
                            user=str(getattr(my_config, "user")),
                            password=str(getattr(my_config, "password")),
                            show_startup_banner=True
                            )
        print("Connected to Milvus!")
        # Check if the server is ready.
        print("Version:" + str(utility.get_server_version()))
        return connection_alias
    except Exception as e:
        print("Problem in connecting to Milvus")
        print(e)
        sys.exit(0)


def delete_role(role_name):
    try:
        connection_alias = connect_to_milvus("default")
        role = Role(role_name, using=connection_alias)
        if role.is_exist():
            granted_collections = role.list_grants()
            granted_collection_list = [i.object_name for i in granted_collections.groups]
            for _collection in granted_collection_list:
                role.revoke("Collection", _collection, "*")
            role.revoke("Global", "*", "*")
            user_role = role.get_users()
            for user_name in user_role:
                role.remove_user(user_name)
            role.drop()
        else:
            print("Role doesn't exists")
        connections.disconnect(connection_alias)
    except Exception as e:
        print(e)


def delete_user(user_name):
    connection_alias = connect_to_milvus("default")
    utility.delete_user(user_name, using=connection_alias)
    connections.disconnect(connection_alias)


if __name__ == '__main__':
    delete_role("my_team1_role")
    delete_role("my_team2_role")
    delete_role("my_team3_role")
    delete_user("my_team1_usr")
    delete_user("my_team2_usr")
    delete_user("my_team3_usr")
