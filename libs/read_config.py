import configparser


class ReadConfig:

    def __init__(self, *config_file):
        self.config_file = config_file
        self.config = configparser.ConfigParser()
        self.config.optionxform = str
        self.total_teams = 0
        file = self.config.read(self.config_file)
        if not file:
            raise ValueError("Config file not found!!")
        for section in self.config.sections():
            if "TEAM" in section:
                self.total_teams = self.total_teams + 1
            self.__dict__.update(self.config.items(section))


if __name__ == '__main__':
    my_config = ReadConfig("config/config.ini")
    print(my_config.host)
    print(my_config.port)
