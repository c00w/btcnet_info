try:
    import ConfigParser
except:
    import configparser as ConfigParser
    
import gevent, baseobject

class Coin(baseobject.Base_Object):
    
    def _setup_general(self, section):
        self.general_info = section
        self.name = section.get('short_name', 'Unknown')
        self.long_name = section.get('long_name', 'Unknown')
        
    def _poll(self):
        pass
