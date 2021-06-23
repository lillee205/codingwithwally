from model import User 
from initialize import db, bcrypt

def initAdminAcc():
    accounts = [User(email = "zdodds@hmc.edu", password = "WeLoveCS!", admin = True)]
    for user in accounts:
        #if user doesn't exist in db, add
        if db.session.query(User.id).filter_by(email = user.email).first() is None:
            #hash password for security reasons
            user.password = bcrypt.generate_password_hash(user.password).decode("utf-8")
            db.session.add(user)
            db.session.commit()
