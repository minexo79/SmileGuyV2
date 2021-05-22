import yaml, configparser


class yamlhook:
    __slots__ = ['filename']

    def __init__(self, filename):
        self.filename = filename

    # load : 純讀取
    # operate: 操作

    def load(self):
        with open(self.filename, 'r', encoding="utf8") as yd:
            return yaml.safe_load(yd)

    def Operate(self, dictTopic: str, setting):
        with open(self.filename, 'r', encoding="utf8") as yd:
            data = yaml.safe_load(yd)

        data[dictTopic] = setting

        with open(self.filename, 'w', encoding="utf8") as yd:
            yaml.safe_dump(data, yd)


class confighook:
    __slots__ = ['filename', '_botParameter']

    def __init__(self, filename):
        self.filename = filename
        _config = configparser.ConfigParser()
        _config.read(self.filename)

        self._botParameter = _config['BOT']

    @property  # Bot Version
    def botVersion(self) -> str:
        return str(self._botParameter['version'])

    @property  # Bot Prefix
    def botPrefix(self) -> str:
        return str(self._botParameter['prefix'])

    @property  # Bot Token
    def botToken(self) -> str:
        return str(self._botParameter['token'])
