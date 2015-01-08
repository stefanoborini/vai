import copy
import os
import json
import locale

def _defaultConfigPath():
    """
    Returns the default configuration path in agreement with XDG rules
    """
    home = os.path.expanduser('~')
    xdg_config_home = os.environ.get('XDG_CONFIG_HOME') or \
                      os.path.join(home, '.config')
    config_dir = os.path.join(xdg_config_home, 'vai')
    if not os.path.isdir(config_dir):
        os.makedirs(config_dir)
    return os.path.join(config_dir, 'vairc')

class Configuration:
    DEFAULTS = {
                 "colors.syntax_schema"     : "default",
                 "colors.status_bar.fg"     : "yellow",
                 "colors.status_bar.bg"     : "darkblue",
                 "colors.side_ruler.fg"     : "darkcyan",
                 "colors.side_ruler.bg"     : "transparent",
                 "icons.collection"         : "unicode1",
                 }

    # Singleton
    _instance = None

    # The file where to read the data
    _filename = None

    flags = { "has_wide_ncurses" : True }

    @classmethod
    def instance(cls):
        if cls._instance is None:
            cls._instance = cls()
        return cls._instance

    @classmethod
    def setFilename(cls, filename):
        if cls._instance is not None and self._filename is not None:
            raise Exception("Configuration already initialized")

        cls._filename = filename

    @classmethod
    def filename(cls):
        if cls._filename is None:
            cls._filename = _defaultConfigPath()
        return cls._filename

    @classmethod
    def save(cls):
        config = cls.instance()
        with open(cls._filename, "w") as f:
            f.write(json.dumps(config._config_dict, indent=4, sort_keys=True))

    def __init__(self):
        cls = self.__class__
        filename = cls.filename()

        try:
            with open(filename, "r") as f:
                merge_data = json.loads(f.read())
        except:
            merge_data = {}

        self._config_dict = copy.deepcopy(Configuration.DEFAULTS)
        self._config_dict.update(merge_data)

    def __getitem__(self, key):
        return self._config_dict[key]

    @classmethod
    def get(cls, key):
        # We override, but not alter, the configuration if the current encoding
        # is not supporting utf-8 encoding, or if we don't have wide ncurses
        if (key == "icons.collection" and locale.getpreferredencoding(False) != "UTF-8") \
            or not cls.flags.get("has_wide_ncurses"):
            return "ascii"
        return cls.instance()[key]



