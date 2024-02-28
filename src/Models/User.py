from neomodel import StructuredNode, StringProperty,IntegerProperty,ArrayProperty


class User(StructuredNode):
    name = StringProperty()
    client_id=IntegerProperty(unique=True,required=True,unique_index=True)
    profile=ArrayProperty()
    favorite_description=ArrayProperty()


