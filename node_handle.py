import logging, traceback, json, re, time

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
        
    def json_ec(self, Node, value, _):
        return self.json(Node, value, _)
        
    def json(self, Node, value, _):
        """
        Handles json method of polling
        """
        
        try:
            item = json.loads(value)
        except:
            logging.debug(value)
            raise
        
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
        Node.dict['key'] = Node.dict['key'].replace('\\r', '\r').replace('\\n', '\n').replace('\\\\d', '\d')
       
        result = re.search( Node.dict['key'], str(resp))
        if not result:
            #raise ValueError('%s: No matching re %s, %s' 
            #        % (Node.name, len(resp), Node))
            return
            
        group = int(Node.dict['group']) if 'group' in Node.dict else 1
        result = result.group(group)
        
        if 'strip' in Node.dict and type(result) is str:
            result = result.replace(Node.dict['strip'][1:-1], '')
        return result
        
    def rate(self, Node, info, source):
        if source == 'rate':
            """
            If this is the rate just update it
            """
            def scale_to_mult(scale):
                scale = scale.lower()
                if scale == 'gh':
                    return 1000**3
                elif scale == 'mh':
                    return 1000 ** 2
                elif scale == 'kh':
                    return 1000
                return 1
            
            rate = float(info)
            mode = Node.namespace.get_node('rate').dict['scale']
            
            hashs = rate * scale_to_mult(mode)
            Node.dict['rate'] = hashs
            return Node.dict.get('value', None)
            
        if source[0:4] == 'time':
            """
            If this is the increment timer increase the shares
            """
            
            #Figure out how long it has been
            old_time = float(Node.dict.get('last_called', time.time()))
            new_time = float(time.time())
            diff = new_time - old_time
            Node.dict['last_called'] = new_time
            
            #Add to shares
            shares = float(Node.dict.get('value', 0))
            rate = float(Node.dict.get('rate', 0))
            new = shares + float(rate)/(2**32) * diff
            return new

        
    def rateduration(self, Node, value, resp):
        if resp == 'rate':
            """
            If this is the rate just update it
            """
            self.rate(Node, value, resp)
            
        elif resp == 'duration':
            """
            If this is duration check for a drop
            """
            if 'rate' not in Node.dict:
                return
            
            rate = float(Node.dict['rate'])
            
            old_dur = Node.dict.get('duration', 0)
            Node.dict['duration'] = float(value)
            
            if float(value) < old_dur:
                return 0
            else:
                diff = float(value) - float(old_dur)
                return float(Node.dict.get('value', 0)) + float(rate)/(2**32) * float(diff)
            
    def difficulty(self, Node, _, __):
         #Difficulty Sites
        if 'coin' not in Node.dict:
            raise ValueError("No coin in node")
            
        coin = Node.dict['coin']
        diffs = []
        for site in Node.objects.difficulty_sites:
            if site[coin]:
                try:
                    float(site[coin])
                except:
                    continue
                diffs.append(site[coin])
        return _median(diffs)
        
    def exchange(self, Node, _, __):
        #Exchange Sites
        
        if 'coin' not in Node.dict:
            raise ValueError("No coin in node")
            
        coin = Node.dict['coin']
        exchange = []
        for site in Node.objects.exchanges:
            if getattr(site, coin, None):
                exchange.append(getattr(site, coin, None))
           
        exchange = _median(exchange)
        if not exchange and Node.name == 'btc':
            return '1.0'
        return exchange
        
        
    def duration(self, Node, value, __):
        def prefix_multiplier(prefix):
            if prefix == 'day':
                return 24*60*60
            if prefix == 'hour':
                return 60*60
            if prefix == 'min':
                return 60
            if prefix == 'sec':
                return 1
            return 1
            
        if 'key' not in Node.dict:
            raise ValueError("No key in node")
        if 'items' not in Node.dict:
            raise ValueError("No items in node")
            
        result = re.search(Node.dict['key'], value)
        
        if not result:
            return
            
        times = Node.dict['items'].split(',')
        
        duration = 0
        index = 0
        for prefix in times:
            index += 1
            try:
                duration += float(result.group(index)) * prefix_multiplier(prefix)
            except TypeError:
                logging.debug('Potential type error %s, %s' % (result.group(index), traceback.format_exc()))
        return duration
        
        
handler = Handler()

def handle(Node, value, source):
    """
    Returns a processed value.
    """
    if 'method' not in Node.dict:
        raise ValueError('No method in node')
    method = Node.dict['method']
    
    func = getattr(handler, method, None)
    if not func:
        raise ValueError('Not a valid function %s' % method)
        
    try:
        return func(Node, value, source)
    except:
        string = "Node: %s\n" % Node
        logging.debug(string + traceback.format_exc())
        return None
