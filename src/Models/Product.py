from neomodel import StructuredNode, StringProperty, ArrayProperty,FloatProperty, IntegerProperty


class Product(StructuredNode):
    name = StringProperty(required=True)
    client_id=IntegerProperty(unique_index=True,required=True)
    profile=ArrayProperty()
    embedding=ArrayProperty(FloatProperty())
    brand=StringProperty()
    color=StringProperty()
    type=StringProperty()    
    
    def serialize(self):
        return{
            "id":self.client_id,
            "name":self.name,
            "brand":self.brand,
            "type":self.type,
            "color":self.color
        }
    
    