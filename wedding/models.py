from wedding import db


class Party(db.Model):
    __tablename__ = 'party'

    id = db.Column(db.Integer, primary_key=True)
    party_name = db.Column(db.String(255))
    invited = db.Column(db.Integer)
    received_gift = db.Column(db.Boolean)
    gift = db.Column(db.Text)
    address = db.Column(db.Text)
    attendees = db.relationship('Attendee',
            backref=db.backref('party', lazy='dynamic'))


class Attendee(db.Model):
    __tablename__ = 'attendee'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    party_id = db.Column(db.Integer, db.ForeignKey('party.id'))
    attending = db.Column(db.Boolean)
