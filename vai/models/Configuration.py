import copy
import contextlib
import json

class Configuration:
    DEFAULTS = {
                 "colors.status_bar.fg"     : "darkcyan",
                 "colors.status_bar.bg"     : "darkblue",
                 "colors.side_ruler.fg"     : "darkcyan",
                 "colors.side_ruler.bg"     : "black",
                 "icons.collection"         : "unicode1",
                 }

    _instance = None

    @classmethod
    def instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    @classmethod
    def initFromFile(cls, filename):
        if cls._instance is None:
            with contextlib.closing(open(filename,"r")) as f:
                merge_data = json.loads(f.read())

            cls._instance = cls(merge_data)

        return cls.instance()


    @classmethod
    def saveAs(cls, filename):
        config = cls.instance()
        with contextlib.closing(open(filename,"w")) as f:
            f.write(json.dumps(config._config_dict))

        if cls._instance is not None:
            cls._instance = cls()

    def __init__(self, merge_data=None):

        self._config_dict = copy.deepcopy(Configuration.DEFAULTS)
        if merge_data is not None:
            self._config_dict.update(merge_data)

    def __getitem__(self, key):
        return self._config_dict[key]

    @classmethod
    def get(cls, key):
        return cls.instance()[key]



