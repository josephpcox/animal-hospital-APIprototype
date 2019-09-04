from flask import Flask
import os
app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!"

app.run(host= '0.0.0.0', port= os.environ.get("PORT", 5000))