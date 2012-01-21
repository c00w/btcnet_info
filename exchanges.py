try:
    import ConfigParser
except:
    import configparser as ConfigParser
    
import gevent, baseobject

class Exchange(baseobject.Base_Object):
    def __init__(self, configfile, objects):
        self.objects = objects
        for coin in self.objects.coins_dict:
            setattr(self, '_setup_%s' % coin, lambda section: self._setup_coin(section, coin))
            
        baseobject.Base_Object.__init__(self, configfile)
            
    def _setup_coin(self, section, coin):
        setattr(self, coin + '_info', section)
            
    def _setup_general(self, section):
        self.general_info = section
        self.name = section.get('name', 'Unknown')
        
    def _poll(self):
        """
        Gets the appropriate values
        """
