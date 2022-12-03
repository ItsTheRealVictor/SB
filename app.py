from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

db = SQLAlchemy(app)
app.app_context().push()

migrate = Migrate(app, db)



class Pet(db.Model):
    """Pet."""

    __tablename__ = "pets"

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    name = db.Column(db.String(50),
                     nullable=False,
                     unique=True)
    species = db.Column(db.String(30), nullable=True)
    hunger = db.Column(db.Integer, nullable=False, default=20)

    def greet(self):
        """Greet using name."""

        return f"I'm {self.name} the {self.species or 'thing'}"

    def feed(self, units=10):
        """Nom nom nom."""

        self.hunger -= units
        self.hunger = max(self.hunger, 0)

    def __repr__(self):
        """Show info about pet."""

        p = self
        return f"<Pet {p.id} {p.name} {p.species} {p.hunger}>"

    @classmethod
    def get_by_species(cls, species):
        """Get all pets matching that species."""

        return cls.query.filter_by(species=species).all()
    
names = [
    'biggie',
    'keko',
    'roger'
]
species = [
    'dog',
    'cat',
    'bird'
]
# together = [Pet(name=n, species=s) for n, s in zip(names, species)]
# db.session.add_all(together)
# db.session.commit()

    
@app.route('/')
def list_pets():
    pets = Pet.query.all()
    return render_template('list.html', pets=pets)

@app.route('/<int:pet_id>')
def show_details(pet_id):
    '''show details about a single pet'''
    shown_pet = Pet.query.get(pet_id)
    return render_template('details.html', shown_pet=shown_pet)

@app.route('/', methods=['POST'])
def make_pet():
    name = request.form.get('name')
    species = request.form.get('species')
    hunger = request.form.get('hunger')
    
    data = Pet(name=name, species=species, hunger=hunger)
    db.session.add(data)
    db.session.commit()
    return redirect('/')