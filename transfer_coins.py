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
    with open('./difficulty_sites/%s' % item, 'wb') as configfile:
        config.write(configfile)
        
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
    config.add_section('api')
    for k,v in pool_info.items():
        if 'api' in k and 'duration' not in k and 'ghashrate' not in k:
            k = k.replace('api_','')
            config.set('api', k, v)
            
    added = False
    for k,v in pool_info.items():
        if 'api' in k and 'duration' in k:
            if not added:
                config.add_section('duration')
                added = True
            k = k.replace('api_', '')
            k = k.replace('_duration', '')
            if k == 'key_hour_min':
                k = 'key'
                config.set('duration', 'hour_group', 1)
                config.set('duration', 'min_group', 2)
            
            config.set('duration', k, v)
            config.set('duration', 'method', pool_info['api_method'])
            
    added = False
    for k,v in pool_info.items():
        if 'api' in k and 'ghashrate' in k:
            if not added:
                config.add_section('ghash')
                added = True
            k = k.replace('api_', '')
            k = k.replace('_ghashrate', '')
            config.set('ghash', k, v)
    if added:
        config.set('ghash', 'method', pool_info['api_method'])
    
    config.add_section('payout')
    for k,v in pool_info.items():
        if 'payout' in k:
            k = k.replace('payout_','')
            config.set('payout', k, v)
            
    for section in ['duration','ghash']:
        if section not in config.sections():
            continue
        if 'address' not in config.items(section):
            config.set(section, 'address', config.get('api','address'))
        if 'strip' not in config.items(section) and 'strip' in dict(config.items('api')):
            config.set(section, 'strip', config.get('api','strip'))
            
            
    config.add_section('shares')
    if pool_info['api_method'] in ['json', 're', 'json_ec']:
        config.set('shares', 'method', 'direct')
    else:
        config.set('shares', 'method', pool_info['api_method'].replace('re_',''))
        
    with open('./pools/%s' % item, 'wb') as configfile:
        config.write(configfile)
