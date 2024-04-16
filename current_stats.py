from pymilvus import (connections, utility)
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
                            host=str(my_config.host),
                            port=int(my_config.port),
                            user=str(my_config.user),
                            password=str(my_config.password),
                            show_startup_banner=True
                            )
        log.info("Connected to Milvus!")
        # Check if the server is ready.
        log.info("Version:" + str(utility.get_server_version()))
        return connection_alias
    except Exception as e:
        log.error("Problem in connecting to Milvus")
        log.critical(e)
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


def list_collections(log):
    try:
        connection_alias = connect_to_milvus("default", logger)
        all_collections = utility.list_collections()
        log.info(all_collections)
        connections.disconnect(connection_alias)
        log.info("Disconnected from Milvus!")
    except Exception as e:
        log.error("Problem in listing users")
        log.critical(e)


if __name__ == '__main__':
    logger_class = LoggerClass()
    logger = logger_class.set_logger()
    list_users(logger)
    list_collections(logger)
