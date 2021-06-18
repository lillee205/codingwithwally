from database import db


class Problem(db.Model):
    __table_args__ = {'extend_existing': True}
    func_name = db.Column("func_name", db.String(50), primary_key = True)
    func_call = db.Column(db.String(70), nullable = False)
    author = db.Column(db.String(40), nullable = False)
    desc = db.Column(db.String, nullable = False)
    testInputs = db.Column(db.String, nullable = False)
    testInputAnswers = db.Column(db.String, nullable = False)
    tags = db.Column(db.String, nullable = False)
    function = db.Column(db.String, nullable = False)
    
    def __repr__(self):
        return """
            func_name = {func_name}\n
            function = {function}\n
            inputs = {inputs}\n
            outputs = {outputs}\n
            tags = {tags}\n
        """.format(func_name =self.func_name, function = self.function, inputs = self.testInputs, outputs = self.testInputAnswers, tags = self.tags)
