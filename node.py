import gevent, logging, httplib2, traceback, node_handle

class Node_NameSpace():
    """
    Class representing a name space of nodes
    Used primarily for name resultion
    """
    
    def __init__(self):
        self.nodes = {}
        
    def get_node(self, name):
        if name in self.nodes:
            return self.nodes[name]
        return None
        
    def add_node(self, node):
        if node.name in self.nodes:
            raise KeyError('Duplicate Name')
        self.nodes[node.name] = node
    

class Node():
    """
    A class representing a node in the information processing chain
    Takes in a dictionary where source is the source node
    Has a set of hooks which are functions to be called on function change
    Also has the ability to produce a dictionary describing its internal state
    """
    
    def __init__(self, name, source_dict, namespace):
        self.name = name
        self.dict = source_dict
        self.hooks = set()
        self.namespace = namespace
        self.namespace.add_node(self)
        self._set_source()
        
    def _set_source(self):
        """
        Add ourselves to the update list
        """
        if 'source' not in self.dict:
            return
            
        source_addr = self.dict['source']
        
        source = self.namespace.get_node(source_addr)
        
        #If this is a web address make a dummy node
        if not source and 'http' in source_addr:
            Http_Node(source_addr, self.namespace)
            source = self.namespace.get_node(source_addr)
            
        if source:
            source.add_hook(self._update_hook)
            
    def add_hook(self, func):
        "Add someone to the hook list"
        self.hooks.add(func)
        if 'value' in self.dict:
            gevent.spawn(func, self.dict['value'])
            
    def _trigger(self):
        "Function to trigger everything in hooks"
        for func in self.hooks:
            gevent.spawn(func, self.dict['value'])
        
    def _update_hook(self, value):
        """
        Called when our source value changes
        """
        #TO BE CHANGED
        output = node_handle.handle(self, value)
        old = getattr(self.dict, 'value', None)
        self.dict['value'] = output
        if old != output:
            self._trigger()
        
        
class Http_Node(Node):
    def __init__(self, addr, namespace):
        self.name = addr
        self.hooks = set()
        self.namespace = namespace
        self.namespace.add_node(self)
        self.dict = {}
        gevent.spawn(self._poll)
        
    def _poll(self):
        """
        Looping functions that pulls values
        """
        Http = httplib2.Http(disable_ssl_certificate_validation=True)
        while True:
            try:
                headers, content = Http.request(self.name)
            except:
                logging.error(traceback.format_exc())
            if content != self.dict['value']:
                self.dict['value'] = content
                self._trigger()
            gevent.sleep(60)
                    
import unittest
class TestNodes(unittest.TestCase):
    def setUp(self):
        import gevent.monkey
        gevent.monkey.patch_all(thread = False, time=False)

    def testNamespace(self):
        namespace = Node_NameSpace()
        node1 = Node('test_node', {'source':'http://github.com'}, namespace)
        self.assertIsNot(namespace.get_node('test_node'), None)
        self.assertIsNot(namespace.get_node('http://github.com'), None)
        addr = namespace.get_node('http://github.com')
        addr.dict['value'] = 'test'
        addr._trigger()
        gevent.sleep(0)
        
        value = node1.dict.get('value', None)
        self.assertEquals(value, 'test')
           
if __name__ == '__main__':
    unittest.main()
            
