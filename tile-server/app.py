from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def index():
    return "<h1>I shall serve you tiles</h1>" 

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)
