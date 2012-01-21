try:
    import ConfigParser
except:
    import configparser as ConfigParser
    
import baseobject

class Site(baseobject.Base_Object):
    """
    Class for difficulty sites.
    """
    
    def __init__(self, configfile, objects):
        for coin in self.objects.coins_dict:
            setattr(self, '_setup_%s' % coin,
                lambda section: self._setup_coin(section, coin))
        self.coins = set()
        baseobject.Base_Object.__init__(self, configfile)
    
    def _setup_general(self, section):
        self.general_info = section
        self.name = section.get('short_name', 'Unknown')
            
    def _setup_coin(self, section, coin):
        setattr(self, coin + '_info', section)
        self.coins.add(coin)
        
    def _poll(self):
        values = self._helper_poll(
            x['name'] + '_info' for x in self.coins
        )
        for k,v in values.items():
            setattr(self, k.split('_')[0], float(v))
