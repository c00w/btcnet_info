"""
Handles all of the update methods and returns a result
"""

import httplib2, socket, traceback, json, re, logging, time

class Wrapper():
    """
    Wrapper class that handles sections. Returns the value for the section
    """
    def __init__(self, site):
        self.object = site
    http = {}
    
    def handle_re_duration(self, info, resp):
        """
        Handles re method of polling
        """
        if 'key' in info:
            resp = getattr(self, 'handle_' + info['key_method'])(info, resp)
       
        if 'key_duration' in info:
            result = re.search( info['key_duration'], resp)
            if not result:
                return
            group = info['group'] if 'group' in info else 1
            result = result.group(group)
        else:
            result = resp
        
        if 'strip' in info  and type(result) is str:
            result = result.replace(info['strip'][1:-1], '')
        return result
    
    def handle_direct(self, info, resp):
        """
        Direct method. Just return the result
        """
        return resp
        
    def handle_re_rateduration(self, info, resp):
        """
        TODO
        """
        pass
            
    def handle_json_ec(self, info, resp):
        """
        TODO or perhaps deprecate
        """
        pass
        
    def handle_re_rate(self, info, resp):
        """
        TODO
        """
        pass
        
    def handle_re_shareestimate(self, info, resp):
        """
        TODO
        """
        pass
            
    def handle_json(self, info, resp):
        """
        Handles json method of polling
        """
        if 'key' not in info:
            raise ValueError('No key in section, %s' % info)
            
        try:
            item = json.loads(resp)
        except ValueError as e:
            #print resp
            #raise e
            return None
        for key in info['key'].split(','):
            item = item[key]
            
        if 'strip' in info and type(item) is str:
        
            item = item.replace(info['strip'][1:-1], '')
        
        return item
        
    def handle_re(self, info, resp):
        """
        Handles re method of polling
        """
        if 'key' not in info:
            raise ValueError('%s: No key in section' % self.object.name) 
       
        result = re.search( info['key'], str(resp))
        if not result:
            raise ValueError('%s: No matching re %s, %s' 
                    % (self.object.name, len(resp), info))
        group = info['group'] if 'group' in info else 1
        result = result.group(group)
        
        if 'strip' in info and type(result) is str:
            result = result.replace(info['strip'][1:-1], '')
        return result
            
    def handle_disable(self, info, resp):
        """
        Disabled pull function
        """
        return
            
    def pull(self, address):
        """
        Pulls web addresses in a sensible manner
        """
            
        if address not in self.http:
            self.http[address] = httplib2.Http(
                    disable_ssl_certificate_validation=True, timeout=10)
            
        headers, resp = self.http[address].request(address, 'GET')
        return resp
        
    def handle_web(self, section):
        """
        Handles web request
        """
        if 'address' not in section or 'method' not in section:
            return
        if section['method'] == 'disable':
            return
        addr = section['address']
        if 'http' not in addr:
            addr = 'http://' + addr
        resp = self.pull(addr)
        method = section['method']
        return getattr(self, 'handle_' + method)(section, resp)
        
    def handlev_direct(self, section):
        """
        returns the direct api
        Used for shares
        """
        if 'api' in self.object.fields:
            return int(self.object.api)
            
    def handlev_rate(self, section):
        """
        Does rate calculations
        """
        prefix = section.get('rate_type', None)
        if prefix:
            
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
        if 'api' not in self.object.fields:
            return
        rate = int(self.object.api)
        rate = rate * mult
        self.object.ghash = float(rate)/(1000**3) 
        rate = float(rate)/2**32
        old = getattr( self.object, '_last_pulled', time.time())
        self.object._last_pulled = time.time()
        diff = self.object._last_pulled- old
        shares = int(rate * diff)
        return shares + getattr(self.object, 'shares', 0)
            
    def handlev_shareestimate(self, section):
        """
        Get share count based on user shares and user reward estimate
        """
        
        if not getattr(self.object, 'api', None):
            return
        response = self.object.api
        
        output = re.search(self.object._config_get('api','key_shares'),
                             response)
        shares = output.group(1)
        
        output = re.search(self.object._config_get('api',
                                     'key_estimate'),response)
        estimate = output.group(1)
        
        round_shares = int(50.0 * float(shares) / float(estimate))
        return int(round_shares) 
            
    def handlev_rateduration(self, section):
        """
        Handles a website with rate and duration
        """
        #Check and assume
        if getattr(self.object, 'ghash', -1) < 0:
            self.object.ghash = 1
            
        old = getattr( self.object, '_last_pulled', time.time())
        self.object._last_pulled = time.time()
        diff = self.object._last_pulled - old
        
        self.object._duration_temporal = getattr(self.object,
                                     '_duration_temporal', 0) + diff
        
        # new round started or initial estimation
        rate = 0.25 * self.object.ghash
        
        duration = getattr(self.object, 'duration', None)
        if not duration:
            return
            
        old_duration = getattr(self.object, 'old_duration', duration)
        
        if duration < old_duration or old_duration < 0: 
            round_shares = int(rate * duration)
        else:
            round_shares = getattr(self.object, 'shares', 0) + int(rate * diff)
        return round_shares

    def handlev_disable(self, section):
        """
        A disabled virtual function
        """
        return

    def handle_virtual(self, section):
        """
        Function that calls the proper virtual functions
        """
        if 'method' not in section:
            return
        return getattr(self, 'handlev_' + section['method'])(section)

    def handle(self, section):
        """
        Calls the proper virtual are real function handler
        """
        try:
            if 'address' in section:
                return self.handle_web(section)
            else:
                return self.handle_virtual(section)
        except (socket.error, httplib2.ServerNotFoundError) as error:
            logging.debug('Network Error: %s', str(error))
            self.object.api_down = True
        except Exception as error:
            #todo, use python logging for this
            self.object.api_down = True
            logging.debug(traceback.format_exc())
