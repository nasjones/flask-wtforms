"""Adopt application."""

from flask import Flask, render_template, request, redirect, flash
from sqlalchemy.exc import IntegrityError
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, Pets
from forms import AddPetForm, EditPetForm

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///adopt'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

app.config['SECRET_KEY'] = "hush"
debug = DebugToolbarExtension(app)

connect_db(app)
db.create_all()


@app.route('/')
def home():
    """Home route for the page to display all pets"""
    pets = Pets.query.all()
    return render_template('home.html', pets=pets)


@app.route('/add', methods=['GET', 'POST'])
def add_pet():
    """Add pet form to create a new pet"""
    form = AddPetForm()

    print(form.validate_on_submit())
    for value in form:
        print(value.data)

    if form.validate_on_submit():
        name = form.name.data
        species = form.species.data
        photo_url = form.photo_url.data
        age = form.age.data
        notes = form.notes.data
        new_pet = Pets(name=name,
                       species=species,
                       photo_url=photo_url,
                       age=age,
                       notes=notes)

        db.session.add(new_pet)
        db.session.commit()
        flash(f"Succesfully registered {new_pet.name}")
        return redirect('/')
    else:
        return render_template('add.html', form=form)


@app.route('/<pet_id>', methods=['GET', 'POST'])
def pet_display(pet_id):
    """Display for pet and allows update"""
    pet = Pets.query.get_or_404(pet_id)
    form = EditPetForm(obj=pet)
    if form.validate_on_submit():
        pet.photo_url = form.photo_url.data
        pet.notes = form.notes.data
        pet.available = form.available.data
        db.session.commit()
        flash("Succesfully updated")
        return redirect(f'/{pet_id}')
    else:
        return render_template('display.html', pet=pet, form=form)
