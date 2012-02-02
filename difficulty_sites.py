"""
File for describing sites we scrape difficulty off of.
"""

import baseobject

class Site(baseobject.Base_Object):
    """
    Class for difficulty sites.
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
                self._setup_coin(section)
    
    def _setup_general(self, section):
        """
        Setup general info.
        Also sets up name
        """
        self.name = section.get('name', 'Unknown')
        self.fields.add('name')
            
    def _setup_coin(self, coin):
        """
        Log that we scrape this coin
        """
        self.coins.add(coin)
            
    def _poll(self):
        for item in self.coins:
            value = self.wrapper.handle(dict(self.config.items(item)))
            if value:
                setattr(self, item, value)
                self.fields.add(item)
            
    def __repr__(self):
        return '<Difficulty Site %s, %s>' % (self.name, str(self.coins))
