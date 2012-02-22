import logging, traceback, json, re

def _median(data):
        """
        Returns the median from a set of data.
        Is not O(1) for memory usage but whatever
        """
        if not data:
            return None
        count = {}
        for item in data:
            if item not in count:
                count[item] = 0
            count[item] += 1
        
        max_count = max(count.values())
        for item in count:
            if count[item] == max_count:
                return item

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
        
        if not resp:
            return
        
        if 'key' not in Node.dict:
            raise ValueError('%s: No key in section' % Node.name) 
       
        #Hacks to deal with wierd parser imports
        Node.dict['key'] = Node.dict['key'].replace('\\\\r', '\r').replace('\\\\n', '\n')
       
        result = re.search( Node.dict['key'], str(resp))
        if not result:
            #raise ValueError('%s: No matching re %s, %s' 
            #        % (Node.name, len(resp), Node))
            return
            
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
           
        return _median(diffs)
        
    def exchange(self, Node, info, resp):
        #Exchange Sites
        exchange = []
        for site in Node.objects.exchanges:
            if getattr(site, Node.name):
                exchange.append(getattr(site, Node.name))
           
        exchange = _median(exchange)
        if not exchange and Node.name == 'btc':
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
        logging.error(Node)
        return value
