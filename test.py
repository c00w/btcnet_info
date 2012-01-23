import unittest
import __init__
import coins
import pools
import gevent

class TestStore(unittest.TestCase):
    def testCoins(self):
        gevent.sleep(10)
        for item in __init__.get_coins():
            self.assertTrue(type(item) is coins.Coin )
            
    def testPools(self):
        gevent.sleep(10)
        for item in __init__.get_pools():
            self.assertTrue(type(item) is pools.Pool )
            
    def testPolling(self):
        gevent.sleep(10)
        count = len(__init__.get_pools())
        shares = 0
        for item in __init__.get_pools():
            if 'shares' in dir(item):
                shares += 1
        print "%s/%s" % (shares, count)
        

if __name__ == "__main__":
    unittest.main()  
