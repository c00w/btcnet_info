import unittest
import __init__
import coins
import pools
import gevent
import json

class TestStore(unittest.TestCase):
    var = None

    @classmethod
    def setUpClass(self):
        __init__.get_coins()
        for i in range(120):
            gevent.sleep(1)
            print i

    def testCoins(self):
        for item in __init__.get_coins():
            self.assertTrue(type(item) is coins.Coin )

    def testPools(self):
        for item in __init__.get_pools():
            self.assertTrue(type(item) is pools.Pool )

    def testMineAddress(self):
        valid = 0
        total = 0
        for item in __init__.get_pools():
            total += 1
            if item['mine.address'] != None:
                valid += 1
        print 'Pools with addresses %s/%s' % (valid, total)

    def testPolling(self):
        count = len(__init__.get_pools())
        shares = 0
        for item in __init__.get_pools():
            try:
                a = float(item.shares)
                shares += 1
            except:
                print 'Invalid Pool: %s' %( item.name)
                pass
        print
        print "Valid Pools %s/%s" % (shares, count)

        count = len(__init__.get_coins())
        shares = 0
        for item in __init__.get_coins():
            if item.exchange:
                shares += 1
        print "Valid Coins w/ Exchanges %s/%s" % (shares, count)

        count = len(__init__.get_coins())
        shares = 0
        for item in __init__.get_coins():
            if item.difficulty:
                print "%s: %s" % (item.name, item.difficulty)
                shares += 1
        print "Valid Coins w/ Difficulty %s/%s" % (shares, count)

    def testApiDifficulty(self):
        for coin in __init__.get_coins():
            float(__init__.get_difficulty(coin.name))

    def testApiExchange(self):
        for coin in __init__.get_coins():
            if coin.exchange:
                float(__init__.get_exchange(coin.name))

    def testBlockInfo(self):
        pool = __init__.get_pool('deepbit')
        print pool.blocks
        assert pool.blocks != None
        assert len(json.loads(pool.blocks))

    def testSetInfo(self):
        __init__.get_pool('deepbit').namespace.get_node('shares').set_value(0)
        assert __init__.get_pool('deepbit').shares == 0


    def testprintSlushShares(self):
        print __init__.get_pool('slush').shares
if __name__ == "__main__":
    unittest.main()
