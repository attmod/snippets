""" Flask application example


"""

from flask import Flask

app = Flask(__name__) # name optional

@app.route("/")
def main():
    return "This is a Python example for a Flask server"

if __name__ == "__main__":
    app.run(host='0.0.0.0',port="8080")
