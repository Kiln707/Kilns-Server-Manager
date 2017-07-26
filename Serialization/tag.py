class Tag:
    def __init__(self,tagInfo=None):
        if tagInfo is None:
            self.dict = {}
        else:
            self.dict = tagInfo

    def addSubTag(self, tag_name):
        if self.keyExists(tag_name):
            return None
        self.dict[tag_name] = Tag()
        return self.dict[tag_name]

    def addData(self, tag_name, value):
        allowedValues = (bool, bytes, chr, complex, float, int, str, dict, frozenset, set, tuple, list, Tag)
        if type(value) not in allowedValues:
            raise ValueError("Please use primitive Types");
        if self.keyExists(tag_name):
            raise ValueError(tag_name,"is in use")
        else:
            self.dict[tag_name] = value
        return value

    def getData(self, tag_name):
        return self.dict[tag_name]

    def removeData(self, tag_name):
        if self.keyExists(tag_name):
            del(self.dict[tag_name])

    def getKeys(self):
        return self.dict.keys()

    def keyExists(self, key):
        if key in self.dict:
            return True
        return False
