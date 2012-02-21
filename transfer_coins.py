"""
Script used to import coins from bitHopper
"""

import ConfigParser

"""
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
"""
"""      
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
    with open('./difficulty_sites/%s' % item, 'wb') as configfile:
        config.write(configfile)
        
"""
parse = ConfigParser.RawConfigParser()
parse.read('../bitHopper/pools.cfg')
parse.read('../bitHopper/user.cfg.default')

for item in parse.sections():
    pool_info = dict(parse.items(item))
    if 'api_method' not in pool_info:
        continue
    config = ConfigParser.RawConfigParser()
    config.add_section('general')
    config.set('general', 'coin', pool_info['coin'])
    config.set('general', 'name', item)
    config.add_section('mine')
    config.set('mine','address', pool_info['mine_address'])
    if 'lp_address' in pool_info:
        config.add_section('lp')
        config.set('lp', 'address', pool_info['lp_address'])
        
    config.add_section('shares')
    for k,v in pool_info.items():
        if 'api' in k and 'duration' not in k and 'hashrate' not in k:
            k = k.replace('api_','')
            if k == 'address':
                k = 'source'
            config.set('shares', k, v)
        elif k == 'api_key_mhashrate':
            config.add_section('mhashrate')
            config.set('mhashrate', 'method', pool_info['api_method'])
            config.set('mhashrate', 'source', pool_info['api_address'])
            config.set('mhashrate', 'key', v)
        elif k == 'api_key_ghashrate':
            config.add_section('ghashrate')
            config.set('ghashrate', 'method', pool_info['api_method'])
            config.set('ghashrate', 'source', pool_info['api_address'])
            config.set('ghashrate', 'key', v)
        elif 'duration' in k:
            print k
        elif 'api' in k and 'hashrate' in k:
            print k
        
    with open('./pools/%s' % item, 'wb') as configfile:
        config.write(configfile)
