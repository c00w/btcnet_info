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
    config.set('general', 'payout_scheme', pool_info.get('payout_scheme','unknown'))
    config.set('general', 'payout_mm', str('payout_merged_mining' in pool_info))
    config.add_section('mine')
    config.set('mine','address', pool_info['mine_address'])
    if 'lp_address' in pool_info:
        config.add_section('lp')
        config.set('lp', 'address', pool_info['lp_address'])
        
    config.add_section('shares')
    
    if 're' in pool_info['api_method']:
        method = 're'
    else:
        method = 'json'
    
    for k,v in pool_info.items():
        if 'api' in k and 'duration' not in k and 'hashrate' not in k:
            k = k.replace('api_','')
            if k == 'address':
                k = 'source'
            config.set('shares', k, v)
            
        elif k == 'api_key_mhashrate':
            config.add_section('rate')
            config.set('rate', 'method', method)
            config.set('rate', 'source', pool_info['api_address'])
            config.set('rate', 'key', v)
            config.set('rate', 'scale', 'mh')
        elif k == 'api_key_ghashrate':
            config.add_section('rate')
            config.set('rate', 'method', method)
            config.set('rate', 'source', pool_info['api_address'])
            config.set('rate', 'key', v)
            config.set('rate', 'scale', 'gh')
        elif k == 'api_key_hashrate':
            config.add_section('rate')
            config.set('rate', 'method', method)
            config.set('rate', 'source', pool_info['api_address'])
            config.set('rate', 'key', v)
            config.set('rate', 'scale', 'h')
        elif k == 'api_key_khashrate':
            config.add_section('rate')
            config.set('rate', 'method', method)
            config.set('rate', 'source', pool_info['api_address'])
            config.set('rate', 'key', v)
            config.set('rate', 'scale', 'kh')
            
        elif 'api_key_duration_' in k:
            fields = k.split('_')[3:]
            config.add_section('duration')
            config.set('duration', 'method', 'duration')
            config.set('duration', 'source', pool_info['api_address'])
            config.set('duration', 'items' , ",".join(fields))
            config.set('duration', 'key', v)
            if 'api_key_duration' in pool_info:
                config.set('duration', 'source', 'duration_pre')
                config.add_section('duration_pre')
                config.set('duration_pre', 'source', pool_info['api_address'])
                config.set('duration_pre', 'method', method)
                config.set('duration_pre', 'key', pool_info['api_key_duration'])
                
            
        elif 'duration' in k:
            print k
        elif 'api' in k and 'hashrate' in k:
            print k
            
    shares_info = dict(config.items('shares'))
    for k,v in shares_info.items():
        if k == 'method' and v == 're_rate':
            config.add_section('rate')
            for k,v in shares_info.items():
                config.set('rate', k, v)
                config.remove_option('shares', k)
            
            #This should be checked
            config.set('rate', 'scale', 'gh')
            
            config.set('rate', 'method', 're')
            
            config.set('shares', 'method', 'rate')
            config.set('shares', 'source', 'rate,time:30')
            
        if k == 'method' and v == 're_rateduration':
            config.set('shares', 'source', 'rate,duration')
            config.set('shares', 'method', 'rateduration')
            
        
    with open('./pools/%s' % item, 'wb') as configfile:
        config.write(configfile)
