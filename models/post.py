from py2neo.ogm import GraphObject, Property

class Post(GraphObject):
    __primarykey__ = "title"

    title = Property()
    content = Property()
    created_at = Property()
