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
      
parse = ConfigParser.RawConfigParser()  
parse.read('../bitHopper/diffwebs.cfg')
for item in parse.sections():
    coin_info = dict(parse.items(item))
    if coin_info['get_method'] == 'regexp':
        coin_info['get_method'] = 're'
    config = ConfigParser.RawConfigParser()
    config.add_section('general')
    config.set('general', 'coin', coin_info['coin'])
    config.set('general', 'name', item)
    coin = coin_info['coin']
    config.add_section(coin)
    config.set(coin, 'address', coin_info['url'])
    config.set(coin, 'method', coin_info['get_method'])
    if 'pattern' in coin_info:
        config.set(coin, 'key', coin_info['pattern'])
    with open('./coins/%s' % item, 'wb') as configfile:
        config.write(configfile)
