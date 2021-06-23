from initialize import db, bcrypt 
from flask import Flask
import os.path
from routes import wally
from socket import gethostname
from model import Problem
from flask_bcrypt import Bcrypt

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///problems.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = "\x0e+\xb2\xc1w\xb6tm\t\x0ey\xe8cj<\xf4S\x8cR\xd2\x87\xd6\x12\xad"
    db.init_app(app)
    bcrypt.init_app(app)
    app.register_blueprint(wally, url_prefix='')
    return app


def setup_database(app):
    with app.app_context():
        #Problem.query.delete()
        #db.session.commit()
        db.create_all()


if __name__ == '__main__':
    app = create_app()
    if not os.path.isfile('/problems.db'):
        setup_database(app)
    if 'liveconsole' not in gethostname():
        app.run(debug = True)
