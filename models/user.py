from py2neo.ogm import GraphObject, Property

class User(GraphObject):
    __primarykey__ = "email"

    name = Property()
    email = Property()
    created_at = Property()
