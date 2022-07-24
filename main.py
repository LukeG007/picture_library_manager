from flask import Flask, render_template, abort
import os
import json
import sqlite3

app = Flask(__name__)
db = sqlite3.connect('db.sqlite')
cur = db.cursor()
cur.execute('CREATE TABLE IF NOT EXISTS libraries(id TEXT, pretty_name TEXT)')
cur.close()
db.commit()
db.close()

def get_libraries():
    db = sqlite3.connect('db.sqlite')
    cur = db.cursor()
    cur.execute('SELECT * FROM libraries')
    libraries_raw = cur.fetchall()
    cur.close()
    db.close()
    libraries = {}
    for library in libraries_raw:
        libraries[library[0]] = library[1]
    return libraries

@app.route('/')
def home():
    return render_template('home.html', libraries=get_libraries())

@app.route('/library/<string:id>')
def library_view(id):
    libraries = get_libraries()
    if not id in libraries:
        abort(404)
    images = os.listdir(os.path.join('static', 'libraries', id))
    return render_template('library.html', images=images, title=libraries[id], id=id)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5473)
