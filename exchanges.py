try:
    import ConfigParser
except:
    import configparser as ConfigParser
    
import gevent, baseobject

class Exchange(baseobject.Base_Object):
    
    def _setup_general(self, section):
        self.general_info = section
        self.name = section.get('name', 'Unknown')
        
    def _poll(self):
        pass
