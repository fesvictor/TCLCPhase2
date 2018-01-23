'''
An example post would be like the following : 
Post = {
    value = 'I support BN!',
    date = '31-12-2017',
    source = 'Facebook',
    related_to = 'BN',
    semantic_value = 1 # 1 = positive, 0 =neutral, -1 = negative
}
'''
from json import JSONEncoder


class Post:
    def __init__(self):
        self.date = ""
        self.value = ""
        self.source = ""
        self.related_to = None
        self.semantic_value = None

    def default(self, o):
        return o.__dict__

    def __str__(self):
        return "date: %s\nvalue: %s\nsource: %s\nrelated_to: %s\nsemantic_value: %s" % (self.date, self.value, self.source, self.related_to, self.semantic_value)
