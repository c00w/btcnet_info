try:
    import ConfigParser
except:
    import configparser as ConfigParser
    
import gevent, baseobject, request_wrapper

class Exchange(baseobject.Base_Object):
    """
    Class representing exchanges
    """
    def __init__(self, configfile, objects):
        
        self.coins = set()
        baseobject.Base_Object.__init__(self, configfile, objects)
            
    def _setup(self):
        #List all sections
        sections = self.config.sections()
        
        #We must have a general section
        if 'general' not in sections:
            raise ValueError('No general info %s' % str(sections))
        
        for section in sections:
            handle = getattr(self, '_setup_' + str(section), None)
            if handle:
                handle(dict(self.config.items(section)))
                
        for section in sections:
            if section in self.objects.coins_dict:
                self._setup_coin(dict(self.config.items(section)), section)
            
    def _setup_coin(self, section, coin):
        self.coins.add(coin)
            
    def _setup_general(self, section):
        self.general_info = section
        self.name = section.get('name', 'Unknown')
        self.fields.add('name')
        
    def _poll(self):
        for item in self.coins:
            value = self.wrapper.handle(dict(self.config.items(item)))
            if value:
                setattr(self, item, value)
                self.fields.add(item)
        
    def __repr__(self):
        return '<Exchange Site %s, %s>' % (self.name, str(self.coins))
