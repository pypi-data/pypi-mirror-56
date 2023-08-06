import io
import configparser


class ConfigItem:

    def __init__(self, config):
        self.__name__ = config.sections()[0]
        self._config = config
        for key, value in config.items(config.sections()[0]):
            setattr(self, key, value)

    def update_config(self):
        """
        Update existing config.
        :return:
        """
        for key, value in self.__dict__.items():
            if not key.startswith("_"):
                self._config[self.__name__][key] = value

    def __setitem__(self, key, value):
        setattr(self, key, value)
        self._config[self.__name__][key] = value

    def __repr__(self):
        return "({type}, {values})".format(type=self.__name__,
           values={k: v for k, v in self.__dict__.items() if not k.startswith("_")})

    @property
    def info(self) -> dict:
        """
        Returns dict of instance public attrs.
        :return: dict
        """
        return {k: v for k, v in self.__dict__.items() if not k.startswith("_")}


class ConfigParser:

    def __init__(self):
        self.sections = {}

    def read(self, file_path):
        """
        Read config file from path.
        :param file_path:
        :return:
        """
        with open(file_path, "r") as config_file:
            raw_config = config_file.read()
        for section in raw_config.strip().split("\n\n"):
            header = section.split("\n")[0].strip()[1:-1]
            section_config = configparser.RawConfigParser(strict=False)
            section_config.read_file(io.StringIO(section))
            if header == "Interface":
                self.sections[header] = ConfigItem(section_config)
            elif self.sections.get(header):
                self.sections[header].append(ConfigItem(section_config))
            else:
                self.sections[header] = [ConfigItem(section_config)]

    def __getitem__(self, item):
        return self.sections.get(item)

    def __setitem__(self, key, value):
        conf = configparser.RawConfigParser()
        conf[key] = value
        if self.sections.get(key):
            self.sections[key].append(ConfigItem(conf))
        else:
            self.sections[key] = [ConfigItem(conf)]

    def __repr__(self):
        repr_string = io.StringIO()
        for section_name, section in self.sections.items():
            if isinstance(section, ConfigItem):
                section.update_config()
                section._config.write(repr_string)
            elif isinstance(section, list):
                for item in section:
                    item.update_config()
                    item._config.write(repr_string)
        return repr_string.getvalue()

    def _update_configs(self, item):
        """
        Update existing config.
        :param item:
        :return:
        """
        if isinstance(item, ConfigItem):
            item.update_config()
        if isinstance(item, list):
            for sub_item in item:
                self._update_configs(sub_item)

    def write(self, io_file):
        """
        Save config to file
        :param io_file: IO
        :return:
        """
        self._update_configs(self.sections)
        io_file.write(self.__repr__())

    def has_section(self, name):
        """
        Check if config has section
        :param name:
        :return:
        """
        return bool(self.sections.get(name))
