"""
Api Class which handles basic manipulation of objects
"""
import objects

class API():
    """
    Wrapper Class for api access
    """
    def __init__(self):
        self.objects = objects.Objects()
        
    def get_coins(self):
        """
        Returns a set of cointypes
        """
        return self.objects.coins
        
    def get_pools(self):
        """
        Returns a set of pools
        """
        return self.objects.pools
        
    def get_difficulty(self, coin_name):
        """
        Returns the difficulty for the coin
        """
        for coin in self.objects.coins:
            if coin.name == coin_name:
                return coin.difficulty
                
        return None
        
    def get_exchange(self, coin_name):
        """
        Returns the difficulty for the coin
        """
        for coin in self.objects.coins:
            if coin.name == coin_name:
                return coin.exchange
                
        return None
        
