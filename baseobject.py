"""
Base object that all sites inherit off of.
"""

try:
    import ConfigParser
except ImportError:
    import configparser as ConfigParser
    
import gevent, traceback, httplib2, socket, request_wrapper, logging

class Base_Object(object):
    """
    Base object for all website classes to inherit off of
    """
    def __init__(self, config_file, objects):
        self.name = ''
        self.objects = objects
        self.config = ConfigParser.RawConfigParser()
        self.config.read(config_file)
        self._poll_rate = 30
        self._alive = True
        self.fields = set()
        self.wrapper = request_wrapper.Wrapper(self)
        self._setup()
        self.api_down = False
        gevent.spawn(self._poll_wrap)
        
    def _poll(self):
        """
        Should be overriden, provides main polling function
        """
        pass
        
    def poll_hook(self):
        """
        Should be left alone so that progams which import the library
        can customize some behavior
        """
        pass
        
    def _setup(self):
        """
        Default setup function.
        Calls self._handle_name for each name in sections
        """
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
        """
        Acts like a getattr for a config section, allows you to specify a
        default paramater if item does not exists
        """
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
            except (socket.error, httplib2.ServerNotFoundError) as error:
                logging.error('%s Network Error: %s' , (self.name, str(error)))
                self.api_down = True
            except Exception:
                #todo, use python logging for this
                self.api_down = True
                traceback.print_exc()
                print self.name + "^^^"
            gevent.sleep(self._poll_rate)
