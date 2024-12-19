from flask import Flask

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///reliox_database.db'

if __name__ == "__main__":
    app.run(debug=True)
