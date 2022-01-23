from calendarweb import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)    
    events = db.relationship("Event", backref="user", lazy=True)
    
    def __repr__(self):
        return f"User('{self.username}, {self.email}')"


class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    type = db.Column(db.String(100), nullable=False)
    duration = db.Column(db.Float, nullable=False)
    date = db.Column(db.String(12), nullable=False)
    color = db.Column(db.String(22), nullable=False)
    activityClass = db.Column(db.String(30), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    