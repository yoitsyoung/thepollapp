from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

class Question(db.Model):
    __tablename__ = "questions"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    date = db.Column(db.String, nullable=True)
    questions = db.relationship("Option", backref = 'options', lazy=True)

    def add_option(self, title, img):
        o = Option(title=title, img=img, question=question.id)
        db.session.add(o)
        db.session.commit()

    def get_options(self):
        for option in self.options:
            print(option)
    def __str__(self):
        return f'On {self.time}, {self.user} asked: {self.title}. '

class Option(db.Model):
    __tablename__ = 'options'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    img = db.Column(db.LargeBinary, nullable=True)
    score = db.Column(db.Integer, default=0)
    question = db.Column(db.Integer, db.ForeignKey("questions.id"), nullable=False)
    
    def __str__(self):
        return f'{self.title}'

    def add_click(self):
        self.score += 1
        db.session.commit()
    
    def get_score(self):
        score = str(f'{self.score}')
        print(f'{score}')