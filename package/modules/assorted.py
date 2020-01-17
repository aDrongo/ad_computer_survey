def getLocation(device,subnet_ip,subnets):
    if (len(device.extensionAttribute2.values) == 0) or (device.extensionAttribute2.value == 'unknown'):
        location = subnets.get(f"{subnet_ip}", 'unknown')
    else:
        location = device.extensionAttribute2.value
    return location

def getGroup(device):
    import re
    group = str((re.search(r'OU=\w+\s*\w*', str(device.distinguishedName))).group(0)).replace("OU=","")
    return group

def compare(filters, data):
    for filter in filters:
        if str(filter) not in str(data):
            pass
        else:
            return False
    return True

def convertRequest(data):
    dictData = {}
    data = (data.split('/'))[-1]
    data = data.split('&')
    #Process each request
    for request in data:
        request = request.split('=')
        dictData[f'{request[0]}'] = f'{request[1]}'
    return dictData

def loadConfig():
    import json
    try:
        with open('config.json') as f:
            config = json.loads(f.read())
        try:
            server_Env = str(config['server_Env'])
            database_Env = str(config['database_Env'])
            user_name_Env = str(config['user_name_Env'])
            user_pass_Env = str(config['user_pass_Env'])
            workers_Env = str(config['workers_Env'])
            search_base_Env = str(config['search_base_Env'])
            search_attributes_Env = config['search_attributes_Env']
            search_filter_Env = config['search_filter_Env']
            subnet_dict_Env = config['subnet_dict_Env']
        except Exception as e:
            raise 'Config file incorrect'
    except Exception as e:
        raise 'Config file not loaded'
    return (
        server_Env,
        database_Env,
        user_name_Env,
        user_pass_Env,
        workers_Env,
        search_base_Env,
        search_attributes_Env,
        search_filter_Env,
        subnet_dict_Env)