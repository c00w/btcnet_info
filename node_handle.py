import logging, traceback, json, re

class Handler():
    def direct(self, Node, value, _):
        """
        Direct method. Just return the result
        """
        return value
        
    def json(self, Node, value, _):
        """
        Handles json method of polling
        """
        
        try:
            item = json.loads(value)
        except ValueError as e:
            return value
        
        if 'key' not in Node.dict:
            raise ValueError('No key in section, %s' % value)
            
        for key in Node.dict['key'].split(','):
            item = item[key]
            
        if 'strip' in Node.dict and type(item) is str:
        
            item = item.replace(Node.dict['strip'][1:-1], '')
        
        return item
    
    def re(self, Node, resp, _):
        """
        Handles re method of polling
        """
        info = Node.dict
        
        if 'key' not in Node.dict:
            raise ValueError('%s: No key in section' % Node.name) 
       
        result = re.search( Node.dict['key'], str(resp))
        if not result:
            raise ValueError('%s: No matching re %s, %s' 
                    % (Node.name, len(resp), Node))
        group = Node.dict['group'] if 'group' in Node.dict else 1
        result = result.group(group)
        
        if 'strip' in Node.dict and type(result) is str:
            result = result.replace(Node.dict['strip'][1:-1], '')
        return result
        
    def rateduration(self, Node, info, resp):
        if resp == 'rate':
            """
            If this is the rate just update it
            """
            self.dict['rate'] = float(info)
            
        elif resp == 'duration':
            """
            If this is duration check for a drop
            """
            old_dur = self.dict.get('duration', 0)
            if int(info) < old_dur:
                self.dict['value'] = 0
            self.dict['duration'] = int(info)
            
        elif resp == 'timer:30':
            """
            If this is the increment timer increase the shares
            """
            
    def difficulty(self, Node, info, resp):
         #Difficulty Sites
        diffs = []
        for site in Node.objects.difficulty_sites:
            if getattr(site, Node.name):
                diffs.append(getattr(site, Node.name))
           
        return self._median(diffs)
        
    def exchange(self, Node, info, resp):
        #Exchange Sites
        exchange = []
        for site in Node.objects.exchanges:
            if getattr(site, Node.name):
                exchange.append(getattr(site, Node.name))
           
        exchange = self._median(exchange)
        if not exchange and self.name == 'btc':
            return '1.0'
        return exchange
    
handler = Handler()

def handle(Node, value, source):
    """
    Returns a processed value.
    """
    if 'method' not in Node.dict:
        return value
    method = Node.dict['method']
    
    func = getattr(handler, method, None)
    if not func:
        return value
        
    try:
        return func(Node, value, source)
    except:
        logging.error(traceback.format_exc())
        return value
