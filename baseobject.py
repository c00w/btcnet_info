try:
    import ConfigParser
except:
    import configparser as ConfigParser
    
import gevent, traceback, httplib2, socket, logging, request_wrapper

class Base_Object(object):
    def __init__(self, config_file, objects):
        self.objects = objects
        self.config = ConfigParser.RawConfigParser()
        self.config.read(config_file)
        self._poll_rate = 30
        self._alive = True
        self.poll_hook = None
        self.fields = set(['poll_hook'])
        self.wrapper = request_wrapper.Wrapper(self)
        self._setup()
        gevent.spawn(self._poll_wrap)
        
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
        
    def _config_get(self, section, option, default=None):
        try:
            return self.config.get(section, option)
        except ConfigParser.NoSectionError:
            return default
        
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
                #logging.error('%s Network Error: %s' % (self.name, str(e)))
                self.api_down = True
            except Exception as e:
                #todo, use python logging for this
                self.api_down = True
                traceback.print_exc()
                print self.name + "^^^"
            gevent.sleep(self._poll_rate)
