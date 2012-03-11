"""
Base object that all sites inherit off of.
"""

try:
    import ConfigParser
except ImportError:
    import configparser as ConfigParser
    
import gevent, traceback, httplib2, socket, request_wrapper, logging
import node, copy, threading, time

class Base_Object(object):
    """
    Base object for all website classes to inherit off of
    """
    def __init__(self, config_file, objects):
        
        self.config = ConfigParser.RawConfigParser()
        self.config.read(config_file)
        self.namespace = node.Node_NameSpace()
        self.write_nodes = set()
        self.file_name = config_file
        self.lock = threading.Lock()
        self.lock.acquire()
        
        thread = threading.Thread(target=self.write_thread)
        thread.daemon = True
        thread.start()
        
        for section in self.config.sections():
            if section != 'general':
                item = node.Node(section, dict(self.config.items(section)), self.namespace, objects)
                self.write_nodes.add(item)
            else:
                values = dict(self.config.items(section))
                for item in values:
                    setattr(self, item, values[item])
                    
        self.lock.release()
                    
    def write_poll(self):
        while True:
            while not self.lock.acquire(False):
                gevent.sleep(0)
            
            for node in self.writes:
                section = node.name
                for k,v in node.get_dict().items():
                    self.config.set(section, k,v)
                    
            self.lock.release()
            gevent.sleep(60)
                        
    def write_thread(self):
        mode = 'wb'
        while True:
            try:
                fd = open(self.file_name, mode)
            except IOError, e:
                return
            with self.lock:
                try:
                    fd.seek(0)
                    self.config.write(fd)
                except IOError as e:
                    fd.close()
                    fd = open(self.file_name, mode)
            time.sleep(60)
                    
    def __getattr__(self, name):
        node = self.namespace.get_node(name)
        if node and 'value' in node.dict:
            return node.dict['value']
        else:
            return None
    
