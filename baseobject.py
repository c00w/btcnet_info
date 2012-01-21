try:
    import ConfigParser
except:
    import configparser as ConfigParser
    
import gevent

class Base_Object(object):
    def __init__(self, config_file):
    
        self.config = ConfigParser.SafeConfigParser()
        print config_file
        self.config.read(config_file)
        self._setup()
        self._poll_rate = 30
        self._alive = True
        gevent.spawn(self._poll_wrap)
        
    def _poll_wrap(self):
        """
        Wrapper around polling which catches and prints exceptions
        """
        while self._alive:
            try:
                self._poll()
            except Exception as e:
                #todo, use python logging for this
                traceback.print_exc()
            gevent.sleep(self._poll_rate)
        
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
