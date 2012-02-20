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
