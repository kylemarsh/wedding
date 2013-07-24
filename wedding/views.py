from flask import flash, redirect, render_template, request, url_for

from wedding import app, db
from wedding.models import Party


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
            parties = Party.query.filter_by(party_name=query).all()
            if len(parties) == 1:
                party = parties[0]
                parties = None
                # populate form

    elif request.method == 'POST':
        try:
            party = Party.query.get(form['party_id'])
            if not party:
                flash('Please try again.')
                raise ValidationError('no party')

            for attendee in party.attendees:
                a_id = attendee.attendee_id
                attending = ('%s_attending' % a_id) in form
                print "Are we attending? %s_attending: %s" % (a_id, attending)
                if attending:
                    print "I'm ATTENDING. LETS VALIDATE"
                    # Let's get validating.
                    name = form['%s_name' % a_id]
                    if name == 'Plus One' or not name:
                        flash("Give your plus one a name!")
                        raise ValidationError()
                    if attendee.name and name != attendee.name:
                        flash("Give your plus one a name!")
                        raise ValidationError()
                    attendee.name = name

                    meal = form['%s_meal' % a_id]
                    print "meal is %s" % meal
                    if meal not in ['0', '1']:
                        flash("Pick meals from the drop-down")
                        raise ValidationError()
                    attendee.meal_choice = meal
                    attendee.attending = True
                else:
                    # They're not coming. Don't validate anything and just
                    # turn them off.
                    print "I'm NOT ATTENDING."
                    attendee.attending = False
            print "no validation errors. Saving..."
            db.session.commit()
            print "saved. flashing..."
            flash("Thanks! Your reservation has been updated")
            print "done. redirecting to ceremony."
            return redirect(url_for('index', _anchor='ceremony'))

            print "wat?"
        except ValidationError:
            print "got a validation error"
            return redirect(url_for('rsvp'))

        print "wat."

    return render_template('rsvp.html', query=query, parties=parties,
            party=party)


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
