try:
    import ConfigParser
except:
    import configparser as ConfigParser
    
import gevent, traceback, httplib2, socket, logging, re, json

class Base_Object(object):
    def __init__(self, config_file):
        
        self.config = ConfigParser.RawConfigParser()
        self.config.read(config_file)
        self._poll_rate = 30
        self._alive = True
        self._urls =  None
        self._http = None
        self.poll_hook = None
        self.api_down = False
        self.fields = set(['api_down', 'poll_hook'])
        self._setup()
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
                self.api_down = False
            except (socket.error, httplib2.ServerNotFoundError) as e:
                logging.error('%s Network Error: %s' % (self.name, str(e)))
                self.api_down = True
            except Exception as e:
                #todo, use python logging for this
                self.api_down = True
                traceback.print_exc()
                print self.name + "^^^"
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
            if not item:
                continue
            headers, self._resp[item] = self._http.request(item, 'GET')
            
        self.values = {}
        
        #handle_stuff
        for item in sections:
            if not getattr(self, item, None):
                continue
                
            info = getattr(self, item)
            if 'address' not in info:
                print info
            resp = self._resp[info['address']]
            
            #Call the correct methods
            if getattr(self, '_poll_' + info['method'], None):
                value = getattr(self, '_poll_' + info['method'])(info, resp)
                self.values[item] =  value
        return self.values
                
    def _poll_direct(self, info, resp):
        return resp
            
    def _poll_json(self, info, resp):
        """
        Handles json method of polling
        """
        if 'key' not in info:
            raise ValueError('%s: No key in section' % self.name)
            
        try:
            item = json.loads(resp)
        except ValueError as e:
            print resp
            raise e
        for key in info['key'].split(','):
            item = item[key]
            
        if 'strip' in info:
            item.replace(info['strip'][1:-1], '')
        
        return item
        
    def _poll_re(self, info, resp):
        """
        Handles re method of polling
        """
        if 'key' not in info:
            raise ValueError('%s: No key in section' % self.name) 
       
        result = re.search( info['key'], resp)
        if not result:
            return
        group = info[group] if 'group' in info else 1
        result = result.group(group)
        
        if 'strip' in info:
            result.replace(info['strip'][1:-1], '')
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
