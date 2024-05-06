#!/usr/bin/python3
""" Starts a Flask web application """
from flask import Flask, render_template
from models import storage

app = Flask(__name__)


@app.route('/states', strict_slashes=False)
def list_states():
    """ Display a HTML page with a list of all states """
    states = storage.all('State')
    return render_template('9-states.html', states=states)


@app.route('/states/<id>', strict_slashes=False)
def show_state(id):
    """ Display a HTML page with a specific state """
    states = storage.all('State')
    key = 'State.' + id
    if key in states:
        state = states[key]
    else:
        state = None
    return render_template('9-states.html', state=state)


@app.teardown_appcontext
def close_db(error):
    """ Remove the current SQLAlchemy Session """
    storage.close()


if __name__ == '__main__':
    """Main Function"""
    app.run(host="0.0.0.0", port=5000)
