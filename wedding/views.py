#from flask import flash, render_template, redirect, request, url_for
from flask import jsonify, render_template

from wedding import app
from wedding.models import Party, Attendee


@app.route("/")
def index():
    return render_template('index.html')


@app.route("/rsvp", methods=['GET'])
def rsvp():
    parties = Party.query.all()
    return render_template('rsvp.html', parties=parties)


@app.route("/rsvp/party_info/<party_id>", methods=['GET'])
def party_info(party_id=None):
    attendees = Attendee.query.filter_by(party_id=party_id)
    return jsonify(attendees=attendees)

#@app.route("/edit/<recipe_id>", methods=['GET', 'POST'])
#def edit_recipe(recipe_id):
    #recipe = Recipe.query.get_or_404(recipe_id)

    #if request.method == 'GET':
        #labels = Label.query.all()
        #return render_template('edit_recipe.html',
                #recipe=recipe, labels=labels)

    #labels = []
    #label_ids = request.form.get(labels)
    #for label_id in label_ids:
        #label = Label.query.get(id)
        #if label is not None:
            #labels.append(label)

    #recipe.labels = labels
    #db.session.commit()
    #flash('Changes to %s saved' % recipe.title)
    #return redirect(url_for('view_recipe', recipe_id=recipe_id))


@app.route("/ceremony", methods=['GET'])
def ceremony():
    return render_template('ceremony.html')


@app.route("/celebration", methods=['GET'])
def celebration():
    return render_template('celebration.html')


@app.route("/registry", methods=['GET'])
def registry():
    return render_template('registry.html')


@app.route("/contact", methods=['GET'])
def contact():
    return render_template('contact.html')


@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404
