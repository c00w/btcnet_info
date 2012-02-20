"""
Represents sites that give us exchange information
"""
    
import baseobject

class Exchange(baseobject.Base_Object):
    """
    Class representing exchanges
    """
        
    def __repr__(self):
        return '<Exchange Site %s, %s>' % (self.name, self.dict)
