"""
Aggregation class to store information about coins
"""
import baseobject

class Coin(baseobject.Base_Object):
    """
    Class for coins.
    """
    
    def __repr__(self):
        return '<Coin %s, %s>' % (self.name, self.dict)
