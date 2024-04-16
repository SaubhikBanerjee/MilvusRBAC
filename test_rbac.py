import unittest
from pymilvus import (connections, utility, Role)
from libs import ReadConfig


class TestRBAC(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print("Setting up unit test - setUpClass")
        my_config = ReadConfig("config/config.ini")
        # Connecting to my local Milvus in docker image.
        cls._connection_alias = connections.connect("default",
                                                    host=str(getattr(my_config, "host")),
                                                    port=int(getattr(my_config, "port")),
                                                    user=str(getattr(my_config, "user")),
                                                    password=str(getattr(my_config, "password")),
                                                    show_startup_banner=True
                                                    )
        # Check if the server is ready.
        print("Milvus Version:" + str(utility.get_server_version()))

    def test_db_connection(self):
        self.assertIsNotNone(str(self._connection_alias), "Test Case: Database connection failed")

    def test_users(self):
        all_users = utility.list_usernames()
        my_config = ReadConfig("config/config.ini")
        for i in range(1, int(my_config.total_teams) + 1):
            usr_str = "team" + str(i) + "_user_name"
            user_name = getattr(my_config, usr_str)
            self.assertIn(user_name, all_users, "User not created: " + user_name)

    def test_roles(self):
        my_config = ReadConfig("config/config.ini")
        for i in range(1, int(my_config.total_teams) + 1):
            role_str = "team" + str(i) + "_role_name"
            role_name = getattr(my_config, role_str)
            role = Role(role_name)
            self.assertTrue(role.is_exist(), "Role not created: " + role_name)

    def test_user_role_mapping(self):
        my_config = ReadConfig("config/config.ini")
        for i in range(1, int(my_config.total_teams) + 1):
            usr_str = "team" + str(i) + "_user_name"
            user_name = getattr(my_config, usr_str)
            role_str = "team" + str(i) + "_role_name"
            role_name = getattr(my_config, role_str)
            role = Role(role_name)
            self.assertTrue(role.is_exist())
            user_role = role.get_users()
            self.assertIn(user_name, user_role,
                          "User Role mapping not created: User- " + user_name + " Role-" + role_name)

    def test_role_collection_mapping(self):
        # This test case can be improved!!
        my_config = ReadConfig("config/config.ini")
        for i in range(1, int(my_config.total_teams) + 1):
            role_str = "team" + str(i) + "_role_name"
            role_name = getattr(my_config, role_str)
            role = Role(role_name)
            self.assertTrue(role.is_exist())
            collection_str = "team" + str(i) + "_collections"
            collections = getattr(my_config, collection_str)
            collection_list = collections.split(",")
            collection_final_list = [_str.strip() for _str in collection_list]
            for _collection in collection_list:
                grant_collection = role.list_grant("Collection", _collection.strip())
                grant_item_object = grant_collection.groups[0]
                collection_names = grant_item_object.object_name
                self.assertIn(collection_names, collection_final_list)

    @classmethod
    def tearDownClass(cls) -> None:
        connections.disconnect("default")


if __name__ == '__main__':
    unittest.main()
