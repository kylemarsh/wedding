from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
import sqlalchemy

app = Flask(__name__)
app.config.from_pyfile('wedding.cfg')

db = SQLAlchemy(app)

from wedding.models import Party, Attendee
import wedding.views

try:
    Party.query.all()
except sqlalchemy.exc.OperationalError:
    #import animalhouse
    testparties = [
            Party(party_name="John and Jane Doe", invited=3,
                received_gift=False, gift=None,
                address='123 E West St., Township ST 54321'),
            Party(party_name="Mary Jane", invited=2, received_gift=False,
                gift=None, address='987 W East St., Metropolis ST 67890')
            ]

    attendees = [
            Attendee(name="John Doe", party=testparties[0], attending=False),
            Attendee(name="Jane Doe", party=testparties[0], attending=False),
            Attendee(name="'Lil Doe", party=testparties[0], attending=False),
            Attendee(name="Mary Jane", party=testparties[1], attending=False),
            Attendee(name=None, party=testparties[1], attending=False),
            ]

    db.create_all()
    for p in testparties:
        db.session.add(p)
    for a in attendees:
        db.session.add(a)
    db.session.commit()
