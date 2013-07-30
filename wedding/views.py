from flask import flash, redirect, render_template, request, url_for
from sqlalchemy import func, or_

from wedding import app, db
from wedding.models import Party, Attendee, LAGuest


# Routes
@app.route("/")
def index():
    return render_template('index.html')


@app.route("/rsvp", methods=['GET', 'POST'])
def rsvp():
    parties = None
    party = None

    query = request.args.get('q')
    form = request.form
    if request.method == 'GET':
        if query:
            parties = search_party(query)
            if len(parties) == 1:
                party = parties[0]
                parties = None
            elif len(parties) == 0:
                flash("Couldn't find a party for '%s'." % query, 'error')

    elif request.method == 'POST':
        try:
            party = Party.query.get(form['party_id'])
            if not party:
                flash('Please try again.', 'error')
                raise ValidationError('no party')

            for attendee in party.attendees:
                a_id = attendee.attendee_id

                attending = int(form['%s_attending' % a_id])
                if attending:
                    # Let's get validating.
                    name = form['%s_name' % a_id]
                    if name == 'Plus One' or not name:
                        flash("Give your plus one a name!", 'error')
                        raise ValidationError()
                    if attendee.name and name != attendee.name:
                        flash("Give your plus one a name!", 'error')
                        raise ValidationError()
                    attendee.name = name

                    meal = form['%s_meal' % a_id]
                    if meal not in ['0', '1', '2']:
                        flash("Pick meals from the drop-down", 'error')
                        raise ValidationError()
                    attendee.meal_choice = meal
                    attendee.attending = True
                else:
                    # They're not coming. Don't validate anything and just
                    # turn them off.
                    attendee.attending = False
            db.session.commit()
            flash("Thanks! Your reservation has been updated", 'success')
            return redirect(url_for('index', _anchor='ceremony'))

        except ValidationError:
            return redirect(url_for('rsvp'))

    return render_template('rsvp.html', query=query, parties=parties,
            party=party)


@app.route("/rsvpla", methods=['GET', 'POST'])
def rsvpla():
    if request.method == 'GET':
        return render_template('rsvpla.html')

    form = request.form
    name = form['name']

    if not name:
        flash('Hey! You need to tell me your name!', 'error')
        return redirect(url_for('rsvpla'))

    guest = LAGuest.query.filter(
            func.lower(LAGuest.name) == name.lower()).first()

    if guest is None:
        guest = LAGuest(name=name)

    guest.attending = form['attending']
    db.session.add(guest)
    db.session.commit()
    flash("Thanks for letting us know!", 'log')
    return redirect(url_for('index', _anchor='celebration'))


@app.route("/ceremony", methods=['GET'])
def ceremony():
    return redirect(url_for('index', _anchor='ceremony'))


@app.route("/celebration", methods=['GET'])
def celebration():
    return redirect(url_for('index', _anchor='celebration'))


@app.route("/registry", methods=['GET'])
def registry():
    return redirect(url_for('index', _anchor='registry'))


@app.route("/contact", methods=['GET'])
def contact():
    return redirect(url_for('index', _anchor='contact'))


@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404


class ValidationError(Exception):
    """Your form validation is bad and you should feel bad"""


# Behavior
def search_party(query):
    # Try exact party match
    party = Party.query.filter_by(party_name=query).first()
    if party:
        return [party]

    # Try exact attendee match
    attendee = Attendee.query.filter(
            func.lower(Attendee.name) == query.lower()).first()
    if attendee:
        return [attendee.party]

    # Search all attendees:
    conditions = [Attendee.name.ilike('%% %s' % part)
            for part in query.split()]
    conditions += [Attendee.name.ilike('%s %%' % part)
            for part in query.split()]
    attendees = Attendee.query.filter(or_(*conditions)).all()

    parties = {}
    for attendee in attendees:
        parties[attendee.party_id] = attendee.party

    return parties.values()
