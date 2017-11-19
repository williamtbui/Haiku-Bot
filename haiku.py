from flask import Flask, render_template, request
from flask_cors import CORS
app = Flask(__name__)
CORS(app)
#@app.route('/')
#def load_form():
#    return  render_template("index.html")
@app.route('/', methods=['POST'])

def load_haiku():
    if request.method == 'POST':
        word =  request.form['word']
        return word
    else:
        return "Hello"

if __name__ == "__main__":
    app.config['DEBUG'] = True
    app.run()
