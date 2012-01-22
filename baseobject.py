try:
    import ConfigParser
except:
    import configparser as ConfigParser
    
import gevent, traceback, httplib2

class Base_Object(object):
    def __init__(self, config_file):
    
        self.config = ConfigParser.RawConfigParser()
        self.config.read(config_file)
        self._setup()
        self._poll_rate = 30
        self._alive = True
        self._urls =  None
        self._http = None
        self.poll_hook = None
        gevent.spawn(self._poll_wrap)
        
    def _poll_wrap(self):
        """
        Wrapper around polling which catches and prints exceptions
        """
        while self._alive:
            try:
                self._poll()
                if self.poll_hook:
                    self.poll_hook()
            except Exception as e:
                #todo, use python logging for this
                traceback.print_exc()
            gevent.sleep(self._poll_rate)
            
    def _helper_poll(self, sections):
        """
        Makes a list of urls we should pull
        Pulls them
        Calls appropriate handler function
        """
        #Get a list of urls we have to pull
        if not self._urls:
            self._urls = set()
            for item in sections:
                if getattr(self, item, None):
                    self._urls.add(getattr(self, item).get('address'))
                    
        #Set up our http object
        if not self._http:
            self._http = httplib2.Http(disable_ssl_certificate_validation=True, timeout=10)
            
        #Get the bodies
        self._resp = {}
        for item in self._urls:
            self._resp[item] = self._http.request(item, 'GET')
            
        self.values = {}
        
        #handle_stuff
        for item in sections:
            if not getattr(self, item, None):
                continue
                
            info = getattr(self, item)
            resp = self._resp[item['address']]
            
            #Call the correct methods
            if getattr(self, '_poll_' + info['method'], None):
                value = getattr(self, '_poll_' + info['method'])(info, resp)
                self.values[item] =  value
                
    def _poll_direct(self, info, resp):
        return resp
            
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
        
    def _setup(self):
        #List all sections
        sections = self.config.sections()
        
        #We must have a general section
        if 'general' not in sections:
            raise ValueError('No general info %s' % str(sections))
        
        for section in sections:
            handle = getattr(self, '_setup_' + str(section), None)
            if handle:
                handle(dict(self.config.items(section)))
        
    def _poll(self):
        pass
