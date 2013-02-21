from flask import Flask
from flask import render_template

app = Flask(__name__)

@app.route("/")
@app.route("/<who>")
def hello(who="Raymond"):
    return render_template("hello.html", who=who)

if __name__ == "__main__":
    app.run(debug=True)
