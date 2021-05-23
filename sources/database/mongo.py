
import pymongo


class mongoOperate:
    def __init__(self, host, usr, pswd):
        self.host = host
        self.usr = usr
        self.pswd = pswd

        self._connect_str = "mongodb+srv://{0}:{1}@{2}".format(self.usr, self.pswd, self.host)
        self._client = None

    def connect(self) -> bool:
        try:
            self._client = pymongo.MongoClient(self._connect_str)
            return True
        except ConnectionError as e:
            return False

    # TODO Sync data with local yaml -> Copy
    # TODO Sync data with local yaml -> Update

    def disconnect(self) -> bool:
        try:
            self._client.close()
            return True
        except ConnectionError as e:
            return False