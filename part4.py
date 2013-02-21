from flask import Flask, render_template, request
from mongokit import Connection, Document

# configuration
MONGODB_HOST = 'localhost'
MONGODB_PORT = 27017

app = Flask(__name__)
app.config.from_object(__name__)

# connect to the database
connection = Connection(app.config['MONGODB_HOST'],
                        app.config['MONGODB_PORT'])

@app.route("/")
def index():
    coll = list(connection['development'].choices.find())
    return render_template("choices.html", choices=coll)

if __name__ == "__main__":
    app.run(debug=True)

def max_length(length):
    def validate(value):
        if len(value) <= length:
            return True
        raise Exception('%s must be at most %s characters long' % length)
    return validate

class Choice(Document):
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

# register the User document with our current connection
connection.register([Choice])
