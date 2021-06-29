from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

db = SQLAlchemy(session_options={"autoflush": False})
bcrypt = Bcrypt()