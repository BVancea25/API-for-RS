from neomodel import StructuredNode, StringProperty,IntegerProperty,RelationshipTo,ArrayProperty, FloatProperty,RelationshipFrom


class User(StructuredNode):
    name = StringProperty(required=True)
    client_id=IntegerProperty(unique_index=True,required=True)
    profile=ArrayProperty()
    favorite_description=ArrayProperty()


