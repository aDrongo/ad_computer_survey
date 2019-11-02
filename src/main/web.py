from flask import Flask, render_template
import sqlalchemy as db
from collections import Counter
from jinja2 import Template
import operator


def rename(var):
    if var == 0:
        return 'good'
    else:
        return 'bad'


app = Flask(__name__)


@app.route("/")
def home():
    host='localhost'
    db_env = 'database.sqlite'

    try:
        engine = db.create_engine(f'sqlite:///{db_env}')
        connection = engine.connect()
        metadata = db.MetaData()
        print('Connected to DB')
    except Exception as e:
        print(e)
    data = connection.execute("SELECT * FROM 'table' ORDER BY 'group' DESC;")
    data = data.fetchall()
    data.sort(key= operator.itemgetter(6))
    locations = connection.execute("SELECT DISTINCT location FROM 'table';")
    locations = locations.fetchall()
    locations.sort(key= operator.itemgetter(0))
    return render_template("home.html", data=data, locations=locations)

if __name__ == "__main__":
    app.run(debug=True)
