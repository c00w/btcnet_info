try:
    import ConfigParser
except:
    import configparser as ConfigParser
    
import gevent, baseobject, httplib2, re, json, time

class Pool(baseobject.Base_Object):
        
    def _setup_general(self, section):
        self.general_info = section
        self.name = section.get('name', 'Unknown')
        self.coin = section.get('coin', 'btc')
        self.url = section.get('url', '')
        self.fields.add('name')
        self.fields.add('coin')
        self.fields.add('url')
        
    def __repr__(self):
        return '<Pool %s, %s, %s>' % (self.name, self.coin, self.url)
        
    def _poll(self):
        """
        Updates a couple of statistics. Has special handling for duration
        """
        
        for item in ['api','ghash', 'duration','shares']: 
            if item not in self.config.sections():
                continue
            value = self.wrapper.handle(dict(self.config.items(item)))
            if value:
                setattr(self, item, value)
                self.fields.add(item)
