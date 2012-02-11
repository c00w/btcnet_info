import gevent.monkey
gevent.monkey.patch_all(thread = False, time=False)

import os, os.path, gevent, pools, exchanges, coins, difficulty_sites, sys

class Objects(object):
    def __init__(self):
        self.pools = set()
        self.exchanges = set()
        self.difficulty_sites = set()
        self.coins = set()
        self.coins_dict = {}
        self._setup()
        
    def _mapping_setup(self):
        """
        Set up a mapping such that we can access coins by name
        for the exchanges
        """
        for coin in self.coins:
            self.coins_dict[coin.name] = coin
    
    def _setup(self):
        """
        Sets up all of our objects correctly
        """
        #Ugly hack to figure out where we are
        try:
            # determine if application is a script file or frozen exe
            if hasattr(sys, 'frozen'):
                FD_DIR = os.path.dirname(sys.executable)
            else:
                FD_DIR = os.path.dirname(os.path.abspath(__file__))
        except:
            FD_DIR = os.curdir
        
        #Parse config files and create objects
        for file_name in os.listdir(os.path.join(FD_DIR,'coins')):
            self.coins.add(coins.Coin(
                reduce(os.path.join, [FD_DIR, 'coins', file_name, ]),
                self,
            ))
            
        #Some files need to know about the coins
            
        self._mapping_setup()
        
        for file_name in os.listdir(os.path.join(FD_DIR,'difficulty_sites')):
            self.difficulty_sites.add(difficulty_sites.Site(
                reduce(os.path.join, [FD_DIR, 'difficulty_sites', file_name]),
                self,
            ))
            
        for file_name in os.listdir(os.path.join(FD_DIR,'exchanges')):
            self.exchanges.add(exchanges.Exchange(
                reduce(os.path.join, [FD_DIR, 'exchanges', file_name]),
                self ,
            ))
        
        for file_name in os.listdir(os.path.join(FD_DIR,'pools')):
            self.pools.add(pools.Pool(
                reduce(os.path.join, [FD_DIR, 'pools', file_name]),
                self
            ))
            
        gevent.sleep(2)
        
        for item in self.coins:
            item._poll()
        
        
if __name__ == "__main__":
    Objects()
    gevent.sleep(1)
