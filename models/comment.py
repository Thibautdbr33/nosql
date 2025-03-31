from py2neo.ogm import GraphObject, Property

class Comment(GraphObject):
    __primarykey__ = "content"

    content = Property()
    created_at = Property()
