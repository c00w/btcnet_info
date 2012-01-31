try:
    import ConfigParser
except:
    import configparser as ConfigParser
    
import baseobject

class Coin(baseobject.Base_Object):
    """
    Class for coins.
    """
    def _median(self, data):
        if not data:
            return None
        count = {}
        median = None
        for item in data:
            if item not in count:
                count[item] = 0
            count[item] += 1
        
        max_count = max(count.values())
        for x in count:
            if count[x] == max_count:
                return x
        
    
    def _setup_general(self, section):
        self.name = section.get('short_name', 'Unknown')
        self.long_name = section.get('long_name', 'Unknown')
        self.difficulty = section.get('recent_difficulty', 1)
        
    def _poll(self):
        """
        Go through each of the difficulty sites and exchange sites.
        See if they have updates. If so average them
        """
        
        #Difficulty Sites
        diffs = []
        for site in self.objects.difficulty_sites:
            if self.name in site.fields:
                diffs.append(getattr(site, self.name))
           
        diff = self._median(diffs)
        if diff:
            self.difficulty = diff
            self.fields.add('difficulty')
        
        #Exchange Sites
        exchange = []
        for site in self.objects.exchanges:
            if self.name in site.fields:
                exchange.append(getattr(site, self.name))
           
        exchange = self._median(exchange)
        if exchange:
            self.exchange = exchange
            self.fields.add('exchange')
        
        if self.name == 'btc' and 'exchange' not in self.fields:
            self.exchange = 1.0
            self.fields.add('exchange')
    
    def __repr__(self):
        return '<Coin %s, %s>' % (self.name, self.long_name)
