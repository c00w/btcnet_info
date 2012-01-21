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
        
    def _setup_mine(self, section):
        self.mine_info = section
        
    def _setup_shares(self, section):
        self.shares_info = section
        
    def _setup_hashrate(self, section):
        self.hashrate_info = section
        
    def _setup_duration(self, section):
        self.duration_info = section
        
    def __repr__(self):
        return '<Pool %s, %s, %s>' % (self.name, self.coin, self.url)
        
    def _poll(self):
        """
        Makes a list of urls we should pull
        Pulls them
        Calls appropriate handler function
        """
        #Get a list of urls we have to pull
        if not self._urls:
            self._urls = set()
            for item in ['shares_info', 'hashrate_info', 'duration_info']:
                if getattr(self, item, None):
                    self._urls.add(getattr(self, item).get('address'))
                    
        #Set up our http object
        if not self._http:
            self._http = httplib2.Http(disable_ssl_certificate_validation=True, timeout=10)
            
        #Get the bodies
        self._resp = {}
        for item in self.urls:
            self._resp[item] = self._http.request(item, 'GET')
            
        #handle_stuff
        for item in ['shares_info', 'hashrate_info', 'duration_info']:
            if not getattr(self, item, None):
                continue
                
            info = getattr(self, item)
            resp = self._resp[item['address']]
            
            #Call the correct methods
            if getattr(self, '_poll_' + info['method'], None):
                value = getattr(self, '_poll_' + info['method'])(info, resp)
                setattr( self, item.split('_')[0], value)
                    
    def _poll_json(self, info, resp):
        """
        Handles json method of polling
        """
        if 'key' not in info:
            raise ValueError('No key in section')
            
        item = json.loads(resp)
        if 'key' in info:
            item = item[info['key']]
        
        return item
        
    def _poll_re(self, info, resp):
        """
        Handles re method of polling
        """
        if 'key' not in info:
            raise ValueError('No key in section')
            
        result = re.search( info['key'], info)
        group = info[group] if 'group' in info else 1
        result = result.group(group)
        
        if 'strip' in info:
            result.replace(info['strip'][1:-2], '')
        return result
            
                
        
