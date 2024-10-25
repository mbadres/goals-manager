from datetime import datetime, timezone

from . import db


class Goal(db.Model):
    __tablename__ = 'goals'

    id = db.Column(db.Integer, primary_key=True)
    department = db.Column(db.Text, nullable=False)
    statement = db.Column(db.Text, nullable=False)
    criteria = db.Column(db.Text, nullable=False)

    histories = db.relationship('History', backref='goal', lazy=True)

    @property
    def current_score(self):
        latest_history = History.query.filter_by(goal_id=self.id).order_by(History.modified_at.desc()).first()
        return latest_history.score if latest_history else None

    @property
    def latest_state(self):
        latest_history = History.query.filter_by(goal_id=self.id).order_by(History.modified_at.desc()).first()
        return latest_history.state if latest_history else None


class History(db.Model):
    __tablename__ = 'histories'

    id = db.Column(db.Integer, primary_key=True)
    goal_id = db.Column(db.Integer, db.ForeignKey('goals.id'), nullable=False)
    score = db.Column(db.Integer, nullable=False)
    state = db.Column(db.Text)
    comment = db.Column(db.Text)
    modified_by = db.Column(db.Text, nullable=False)
    modified_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))
