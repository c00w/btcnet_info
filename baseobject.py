try:
    import ConfigParser
except:
    import configparser as ConfigParser
    
import gevent

class Base_Object(object):
    def __init__(self, config_file):
    
        self.config = ConfigParser.SafeConfigParser()
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
        pass
        
    def _poll(self):
        pass
