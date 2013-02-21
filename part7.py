from flask import Flask, render_template, request
from mongokit import Connection, Document, ObjectId

# configuration
MONGODB_HOST = 'localhost'
MONGODB_PORT = 27017

app = Flask(__name__)
app.config.from_object(__name__)

# connect to the database
connection = Connection(app.config['MONGODB_HOST'],
                        app.config['MONGODB_PORT'])

@app.route("/", methods=["GET"])
def index():
    coll = list(connection.development.choices.find())
    return render_template("choices3.html", choices=coll)

@app.route("/add-choice", methods=["POST"])
def create():
    choice = connection.development.choices.Choice()
    choice['title'] = request.form['title']
    choice['votes'] = 0
    choice.save()

    coll = list(connection.development.choices.find())
    return render_template("choices3.html", choices=coll)

@app.route("/reset-choices")
def reset():
    connection.development.choices.drop()

    coll = list(connection.development.choices.find())
    return render_template("choices3.html", choices=coll)

@app.route("/choice/<cid>/delete")
def delete(cid):
    connection.development.choices.remove({'_id': ObjectId(cid)})

    coll = list(connection.development.choices.find())
    return render_template("choices3.html", choices=coll)

def max_length(length):
    def validate(value):
        if len(value) <= length:
            return True
        raise Exception('%s must be at most %s characters long' % length)
    return validate

@connection.register
class Choice(Document):
    __collection__ = 'choices'
    __database__ = 'development'

    structure = {
        'title': unicode,
        'votes': int,
    }
    validators = {
        'title': max_length(50)
    }
    use_dot_notation = True
    def __repr__(self):
        return '<Choice %r>' % (self.title)

if __name__ == "__main__":
    app.run(debug=True)
