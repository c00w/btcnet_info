import unittest
import __init__
import coins
import pools
import gevent

class TestStore(unittest.TestCase):
    var = None
    
    def setUp(self):
        if not self.var:
            gevent.sleep(5)
            self.var = True
        
    def testCoins(self):
        for item in __init__.get_coins():
            self.assertTrue(type(item) is coins.Coin )
            
    def testPools(self):
        for item in __init__.get_pools():
            self.assertTrue(type(item) is pools.Pool )
            
    def testPolling(self):
        count = len(__init__.get_pools())
        shares = 0
        for item in __init__.get_pools():
            if 'shares' in dir(item):
                shares += 1
        print "Pools with shares: %s/%s" % (shares, count)
        shares = 0
        count = len(__init__.get_coins())
        for item in __init__.get_coins():
            if 'difficulty' in dir(item):
                shares += 1
        print "Coins with difficulty: %s/%s" % (shares, count)

if __name__ == "__main__":
    unittest.main()  
