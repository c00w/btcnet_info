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
        print
        print "Valid Pools %s/%s" % (shares, count)
        
        count = len(__init__.get_coins())
        shares = 0
        for item in __init__.get_coins():
            if 'exchange' in dir(item):
                shares += 1
        print "Valid Coins w/ Exchanges %s/%s" % (shares, count)
        
        count = len(__init__.get_coins())
        shares = 0
        for item in __init__.get_coins():
            if 'difficulty' in dir(item):
                shares += 1
        print "Valid Coins w/ Difficulty %s/%s" % (shares, count)
        

if __name__ == "__main__":
    unittest.main()  
