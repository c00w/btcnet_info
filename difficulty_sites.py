"""
File for describing sites we scrape difficulty off of.
"""

import baseobject

class Site(baseobject.Base_Object):
    """
    Class for difficulty sites.
    """
            
    def __repr__(self):
        return '<Difficulty Site %s>' % (self.name)
        
        
import unittest
class TestNodes(unittest.TestCase):
    def setUp(self):
        import gevent.monkey
        gevent.monkey.patch_all(thread = False, time=False)

    def testNamespace(self):
        pass
           
if __name__ == '__main__':
    unittest.main()
