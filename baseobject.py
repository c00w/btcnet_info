"""
Base object that all sites inherit off of.
"""

try:
    import ConfigParser
except ImportError:
    import configparser as ConfigParser
    
import gevent, traceback, httplib2, socket, logging
import node, copy, threading, time

class Base_Object(object):
    """
    Base object for all website classes to inherit off of
    """
    def __init__(self, config_file, objects):
        
        self.config = ConfigParser.RawConfigParser()
        if not self.config.read(config_file):
            raise LookupError("No such config file")
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
        gevent.spawn(self.write_poll)
                    
    def write_poll(self):
        while True:
            while not self.lock.acquire(False):
                gevent.sleep(0)
           
            for node in self.write_nodes:
                section = node.name
                for k,v in node.get_dict().items():
                    self.config.set(section, k,v)
                    
            self.lock.release()
            gevent.sleep(60)
                        
    def write_thread(self):
        mode = 'wb'
        while True:
            try:
                with self.lock:
                    with open(self.file_name, mode) as fd:
                        self.config.write(fd)
            except IOError, e:
                return
            time.sleep(60)
                    
    def __getattr__(self, name):
        node = self.namespace.get_node(name)
        if node and 'value' in node.dict:
            return node.dict['value']
        elif '.' in name:
            node, index = name.split('.', 1)
            node = self.namespace.get_node(node)
            if node and index in node.dict:
                return node.dict[index]
        return None
        
    def __getitem__(self, name):
        node = self.namespace.get_node(name)
        if node and 'value' in node.dict:
            return node.dict['value']
        elif '.' in name:
            node, index = name.split('.', 1)
            node = self.namespace.get_node(node)
            if node and index in node.dict:
                return node.dict[index]
        elif node:
            return node.dict
        return None
        
    
