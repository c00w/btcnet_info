import unittest
import __init__
import coins
import pools
import gevent

class TestStore(unittest.TestCase):
    def testCoins(self):
        gevent.sleep()
        for item in __init__.get_coins():
            self.assertTrue(type(item) is coins.Coin )
            
    def testPools(self):
        gevent.sleep()
        for item in __init__.get_pools():
            self.assertTrue(type(item) is pools.Pool )

if __name__ == "__main__":
    unittest.main()  
