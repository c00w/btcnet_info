try:
    import ConfigParser
except:
    import configparser as ConfigParser
    
import baseobject

class Site(baseobject.Base_Object):
    """
    Class for difficulty sites.
    """
    
    def _setup_general(self, section):
        self.general_info = section
        self.name = section.get('short_name', 'Unknown')
        
    def _poll(self):
        pass
