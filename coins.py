try:
    import ConfigParser
except:
    import configparser as ConfigParser
    
import baseobject

class Coin(baseobject.Base_Object):
    """
    Class for coins.
    """
    
    def _setup_general(self, section):
        self.general_info = section
        self.name = section.get('short_name', 'Unknown')
        self.long_name = section.get('long_name', 'Unknown')
        self.difficulty = section.get('recent_difficulty', 1)
        
    def _poll_wrap(self):
        """
        Overriding this because we do no polling
        """
        pass
    
    def __repr__(self):
        return '<Coin %s, %s>' % (self.name, self.long_name)
