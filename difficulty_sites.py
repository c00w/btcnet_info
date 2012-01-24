"""
File for describing sites we scrape difficulty off of.
"""

import baseobject

class Site(baseobject.Base_Object):
    """
    Class for difficulty sites.
    """
    
    def __init__(self, configfile, objects):
        self.objects = objects
        for coin in self.objects.coins_dict:
            setattr(self, '_setup_%s' % coin,
                lambda section: self._setup_coin(section, coin))
        self.coins = set()
        baseobject.Base_Object.__init__(self, configfile)
    
    def _setup_general(self, section):
        """
        Setup general info.
        Also sets up name
        """
        self.name = section.get('name', 'Unknown')
        self.fields.add('name')
            
    def _setup_coin(self, section, coin):
        self.coins.add(self.objects.coins_dict[coin])
            
    def __repr__(self):
        return '<Difficulty Site %s, %s>' % (self.name, str(self.coins))
