from main import app
from modules.init import init


if __name__ == "__main__":
    init()
    app.run()