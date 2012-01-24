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
            if 'api' in self.fields:
                return int(self.api)
            return
            
        if method == 'rate':
            if 'rate_type' in self.duration_info:
                prefix = self.duration_info['rate_type']
                if prefix == 'GH':
                    mult = 1000**3
                if prefix == 'MH':
                    mult = 1000**2
                if prefix == 'KH':
                    mult = 1000
                if prefix == 'None':
                    mult = 1
            else:
                mult = 1000**3
            rate = int(self.api)
            rate = rate * mult
            self.ghash = float(rate)/(1000**3) 
            rate = float(rate)/2**32
            old = getattr( self, '_last_pulled', time.time())
            self._last_pulled = time.time()
            diff = self._last_pulled- old
            shares = int(rate * diff)
            return shares + self.shares
            
        if method == 'shareestimate':
            # get share count based on user shares and user reward estimate
            output = re.search(self.api_info['key_shares'],response)
            shares = output.group(1)  
            
            output = re.search(self.api_info['key_estimate'],response)
            estimate = output.group(1)
            
            round_shares = int(50.0 * float(shares) / float(estimate))
            return int(round_shares) 
            
        if method == 'rateduration':
            
            #Check and assume
            if self.ghash < 0:
                self.ghash = 1
                
            old = getattr( self, '_last_pulled', time.time())
            self._last_pulled = time.time()
            diff = self._last_pulled - old
            
            self._duration_temporal = getattr(self, '_duration_temporal', 0) + diff
            
            # new round started or initial estimation
            rate = 0.25 * self.ghash
            
            duration = getattr(self, 'duration', None)
            if not duration:
                return
                
            old_duration = getattr(self, 'old_duration', duration)
            
            if duration < old_duration or old_duration < 0: 
                round_shares = int(rate * duration)
            else:
                round_shares = server['shares'] + int(rate * diff)
            return round_shares
            
        return
        
    def _poll(self):
        """
        Updates a couple of statistics. Has special handling for duration
        """
        
        values = self._helper_poll(
            ['api_info', 'ghash_info', 'duration_info']
        )
        
        
        for k,v in values.items():
            if v:
                setattr( self, k.split('_')[0], v)
                self.fields.add(k.split('_')[0])
            
        shares = self._handle_shares()
        if shares:
            self.shares = shares
            self.fields.add('shares')
           
                
        
