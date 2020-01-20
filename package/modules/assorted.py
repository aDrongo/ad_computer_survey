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

def rename(var):
    if var == 0:
        return 'good'
    else:
        return 'bad'

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


header = """
<!DOCTYPE html>
<html>
 <head>
  <meta charset="utf-8" http-equiv="refresh" content="300" >
   <title>LDAP Device Surveyor</title>
    <style>
    ul { margin: 0; padding: 5px 5px 0 5px; float: left; }
    li { display: inline-block; padding: 2px 10px 2px 2px; color: #D9D8D6; vertical-align: middle; }
    html { 
        height: 100%;
        box-sizing: border-box;
    }
    body {
        background-color: #222222;
        color: white;
        font-family: monospace;
        min-height: 95%;
        position: relative;
        font-size: 10px;;
        margin: 0;
        padding: 50px 0 0 0;
      }
    a, a:link, a:visited, a:active {
        color: inherit;
        text-decoration: none;
      }
    a:hover{
        color: inherit;
        text-decoration: underline;
      }
    nav {
        position: fixed;
        margin: 0;
        font-size: 16px;
        background-color: #565557;
        width: 100%;
        overflow: hidden;
        box-sizing: border-box;
        display: inline-block;
        transition: all 0.2s;
        list-style-type: none;
        padding-left: 1%;
        top: 0;
    }
    </style>
 </head>
  <body>
    <nav>
      <ul>
        <li><img height="30px" src="https://cdn.nwmsrocks.com/img/3dc41c7.png"/></li>
        <li><a href="/">Overview</a></li>
      </ul>
    </nav>
    <div>
"""