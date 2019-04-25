import json


class Config:
    """Stores a config's contents"""
    def __init__(self, cfgname):
        self.cfgname = cfgname
        with open(cfgname, 'r') as cfg:
            self.content = json.loads(cfg.read())

    def get(self, name):
        """Return an item"""
        return self.content[name]

    def set(self, name, value):
        """Changes the value of an item"""
        self.content[name] = value

    def save(self):
        """Saves edits"""
        with open(self.cfgname, 'w') as cfg:
            cfg.write(json.dumps(self.content, indent=4))
