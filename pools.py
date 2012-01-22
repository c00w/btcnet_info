try:
    import ConfigParser
except:
    import configparser as ConfigParser
    
import gevent, baseobject, httplib2, re, json

class Pool(baseobject.Base_Object):
        
    def _setup_general(self, section):
        self.general_info = section
        self.name = section.get('name', 'Unknown')
        self.coin = section.get('coin', 'btc')
        self.url = section.get('url', '')
        self.fields.add('name')
        self.fields.add('coin')
        self.fields.add('url')
        
    def _setup_mine(self, section):
        self.mine_info = section
        
    def _setup_api(self, section):
        self.api_info = section
        
    def _setup_shares(self, section):
        self.shares_info = section
        
    def _setup_ghash(self, section):
        self.hashrate_info = section
        
    def _setup_payout(self, section):
        self.payout_info = section
        
    def _setup_duration(self, section):
        self.duration_info = section
        
    def __repr__(self):
        return '<Pool %s, %s, %s>' % (self.name, self.coin, self.url)
        
    def _handle_shares(self):
        method = self.shares_info.get('method', None)
        if not method:
            return
        
        if method == 'direct':
            return int(self.api)
            
        if method == '':
            return
            
        return
        
    def _poll(self):
        """
        Updates a couple of statistics. Has special handling for duration
        """
        values = self._helper_poll(
            ['api_info', 'ghash_info', 'duration_info']
        )
        
        for k,v in values.items():
                setattr( self, k.split('_')[0], v)
                self.fields.add(k.split('_')[0])
            
        self.shares = self._handle_shares()
        self.fields.add('shares')
           
                
        
