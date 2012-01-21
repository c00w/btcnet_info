"""
Script used to import coins from bitHopper
"""

import ConfigParser

parse = ConfigParser.SafeConfigParser()
parse.read('../bitHopper/whatevercoin.cfg')
for item in parse.sections():
    coin_info = dict(parse.items(item))
    for k in coin_info.keys():
        if 'exchange' in k:
            del coin_info[k]
    
    config = ConfigParser.SafeConfigParser()
    config.add_section('general')
    for k,v in coin_info.items():
        config.set('general', k, v)
    with open('./coins/%s' % coin_info['short_name'], 'wb') as configfile:
        config.write(configfile)
