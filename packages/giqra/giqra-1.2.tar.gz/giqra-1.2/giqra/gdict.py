from gi.repository.GObject import GObject

class GDict(GObject):
    def __init__(self, *args, **kwargs):
        self.dict = {}
        GObject.__init__(self, *args, **kwargs)
    
    def __getitem__(self, name):
        return self.dict[name]
    
    def __setitem__(self, name, value):
        self.dict[name] = value

