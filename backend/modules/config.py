def load():
    import json
    try:
        with open('config.json') as f:
            configFile = json.loads(f.read())
            return configFile
    except Exception as e:
        print('Config file not loaded')
        raise e

config = load()
