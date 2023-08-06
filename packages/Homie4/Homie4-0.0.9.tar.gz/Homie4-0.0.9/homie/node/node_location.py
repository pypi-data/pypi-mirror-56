from .node_base import Node_Base

from homie.node.property.property_float import Property_Float


class Node_State(Node_Base):

    def __init__(self, device, id='location', name='Location', type_='location', retain=True, qos=1 ): 
        super().__init__(device,id,name,type_,retain,qos)

        self.add_property (Property_Float (self,'latitude','Latitude'))
        self.add_property (Property_Float (self,'longitude','Longitude'))

    def update_state(self,latitude,longitude):
        self.get_property('latitude').value = latitude
        self.get_property('longitude').value = longitude
