from pymilvus import (connections, utility, Role)
from libs import LoggerClass
from libs import ReadConfig
import sys


def connect_to_milvus(connection_alias, log):
    try:
        log.debug("Reading configuration to connect Milvus")
        my_config = ReadConfig("config/config.ini")
        # Connecting to my local Milvus in docker image.
        log.debug("Trying to connect Milvus")
        connections.connect(connection_alias,
                            host=str(getattr(my_config, "host")),
                            port=int(getattr(my_config, "port")),
                            user=str(getattr(my_config, "user")),
                            password=str(getattr(my_config, "password")),
                            show_startup_banner=True
                            )
        log.info("Connected to Milvus!")
        # Check if the server is ready.
        log.info("Version:" + str(utility.get_server_version()))
        return connection_alias
    except Exception as e:
        print("Problem in connecting to Milvus")
        log.error("Problem in connecting to Milvus")
        log.critical(e)
        print(e)
        sys.exit(0)


def list_users(log):
    try:
        connection_alias_usr = connect_to_milvus("default", logger)
        users = utility.list_users(include_role_info=True, using=connection_alias_usr)
        log.info(users)
        connections.disconnect(connection_alias_usr)
    except Exception as e:
        log.error("Problem in listing users")
        log.critical(e)


def create_rbac(log):
    try:
        my_config = ReadConfig("config/config.ini")
        connection_alias = connect_to_milvus("default", logger)
        all_users = utility.list_usernames(using=connection_alias)
        for i in range(1, int(my_config.total_teams) + 1):
            usr_str = "team" + str(i) + "_user_name"
            pass_str = "team" + str(i) + "_passwd"
            user_name = getattr(my_config, usr_str)
            user_password = getattr(my_config, pass_str)
            if user_name in all_users:
                log.info("User already exists, skip:" + str(user_name))
                # utility.delete_user(user_name,using=connection_alias )
            else:
                log.info("Creating user: " + str(user_name))
                utility.create_user(user_name, user_password, connection_alias)
            role_str = "team" + str(i) + "_role_name"
            role_name = getattr(my_config, role_str)
            log.info("Creating Role: " + str(role_name))
            role = Role(role_name, using=connection_alias)
            if not role.is_exist():
                role.create()
            else:
                log.info("Role already exists: " + str(role_name))
            collection_str = "team" + str(i) + "_collections"
            collections = getattr(my_config, collection_str)
            collection_list = collections.split(",")
            log.info("Granting privilege to: " + str(collection_list))
            for _collection in collection_list:
                role.grant("Collection", _collection.strip(), "*")
            log.info("Binding role to the user: " + str(role_name) + " --> " + str(user_name))
            role.add_user(user_name)

        connections.disconnect(connection_alias)
    except Exception as e:
        print(e)


if __name__ == '__main__':
    logger_class = LoggerClass()
    logger = logger_class.set_logger()
    logger.info("Before RBAC run")
    logger.info("****************")
    list_users(logger)
    logger.info("Start RBAC configuration")
    logger.info("*************************")
    create_rbac(logger)
    logger.info("After RBAC run")
    logger.info("****************")
    list_users(logger)
