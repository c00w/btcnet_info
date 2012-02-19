import logging, traceback, json, re

class Handler():
    def direct(self, Node, value):
        """
        Direct method. Just return the result
        """
        return value
        
    def json(self, Node, value):
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
    
    def handle_re(self, Node, resp):
        """
        Handles re method of polling
        """
        info = Node.dict
        
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
    
handler = Handler()

def handle(Node, value):
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
        return func(Node, value)
    except:
        logging.error(traceback.format_exc())
        return value
