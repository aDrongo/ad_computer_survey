from flask import Flask, render_template, Response, redirect, url_for
import sqlalchemy as db
from collections import Counter
from jinja2 import Template
import operator
import sys
import time


def rename(var):
    if var == 0:
        return 'good'
    else:
        return 'bad'


app = Flask(__name__)


@app.route("/")
def home():
    db_env = 'database.sqlite'

    try:
        engine = db.create_engine(f'sqlite:///./{db_env}')
        connection = engine.connect()
        metadata = db.MetaData(bind=connection, reflect=True)
        print('Connected to DB')
    except Exception as e:
        print(e)
        sys.exit(e)
    # print(metadata.tables)
    data = connection.execute("SELECT * FROM 'table' ORDER BY 'group' DESC;")
    data = data.fetchall()
    data.sort(key= operator.itemgetter(6))
    locations = connection.execute("SELECT DISTINCT location FROM 'table';")
    locations = locations.fetchall()
    locations.sort(key= operator.itemgetter(0))
    return render_template("home.html", data=data, locations=locations)
    # return render_template("home.html")

@app.route("/main")
def main():
    import subprocess
    proc = subprocess.Popen(['python3', 'main.py'], stdout=subprocess.PIPE, universal_newlines=True)
    #def inner():
    #    for stdout in iter(proc.stdout.readline, ""):
    #        yield str(stdout) + "<br>\n"
    #    return_code = proc.wait()
    #    if return_code:
    #        return redirect(url_for('home'))
    #return Response(inner(), mimetype='text/html')
    return redirect(url_for('home'))


if __name__ == "__main__":
    app.run(debug=True)
