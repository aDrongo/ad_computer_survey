from main import app
from modules.scheduler import scheduler

if __name__ == "__main__":
    scheduler.start()
    app.run()