from flask import Flask, render_template, abort
import os
import json

app = Flask(__name__)
f = open('libraries.json')
libraries = json.loads(f.read())
f.close()

@app.route('/')
def home():
    return render_template('home.html', libraries=libraries)

@app.route('/library/<string:id>')
def library_view(id):
    if not id in libraries:
        abort(404)
    images = os.listdir(os.path.join('static', 'libraries', id))
    return render_template('library.html', images=images, title=libraries[id], id=id)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5473)
