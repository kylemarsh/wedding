from wedding import db


class Party(db.Model):
    __tablename__ = 'party'

    party_id = db.Column(db.Integer, primary_key=True)
    party_name = db.Column(db.String(255))
    invited = db.Column(db.Integer)
    received_gift = db.Column(db.Boolean)
    gift = db.Column(db.Text)
    address = db.Column(db.Text)
    attendees = db.relationship('Attendee', backref='party',
            lazy='dynamic')


class Attendee(db.Model):
    __tablename__ = 'attendee'

    attendee_id = db.Column(db.Integer, primary_key=True)
    party_id = db.Column(db.Integer, db.ForeignKey('party.party_id'))
    name = db.Column(db.String(255))
    attending = db.Column(db.Boolean)
    meal_choice = db.Column(db.Integer)
    #meal_choice = db.Column(db.Enum('meat', 'fish', 'veggie'))


class LAGuest(db.Model):
    __tablename__ = 'la_guest'

    guest_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    attending = db.Column(db.Boolean)
    gift = db.Column(db.Text)
    received_gift = db.Column(db.Boolean)
    address = db.Column(db.Text)
