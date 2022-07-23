from flask import Flask, render_template
import os

app = Flask(__name__)

@app.route('/')
def home():
    images = os.listdir(os.path.join('static', 'dakota'))
    return render_template('home.html', images=images)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5473)
