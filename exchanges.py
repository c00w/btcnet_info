try:
    import ConfigParser
except:
    import configparser as ConfigParser
    
import gevent, baseobject

class Exchange(baseobject.Base_Object):
    def __init__(self, configfile, objects):
        baseobject.Base_Object.__init__(self, configfile, objects)
        for coin in self.objects.coins_dict:
            setattr(self, '_setup_%s' % coin, lambda section: self._setup_coin(section, coin))
            
        self.coins = set()
       
            
    def _setup_coin(self, section, coin):
        self.coins.add(self.objects.coins_dict[coin])
            
    def _setup_general(self, section):
        self.general_info = section
        self.name = section.get('name', 'Unknown')
        self.fields.add('name')
        
    def __repr__(self):
        return '<Exchange Site %s, %s>' % (self.name, str(self.coins))
