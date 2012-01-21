try:
    import ConfigParser
except:
    import configparser as ConfigParser
    
import gevent, baseobject

class Pool(baseobject.Base_Object):
    
    def _setup(self):
        pass
        
    def _poll(self):
        pass
