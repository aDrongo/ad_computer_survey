from app import AppInitializer
init = AppInitializer()
init.setup()
application = init.get_app()
