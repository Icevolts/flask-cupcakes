"""Flask app for Cupcakes"""
from flask import Flask,render_template,request,jsonify
from models import db,connect_db,Cupcake

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:graygirl@localhost:5433/cupcakes'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'f724'

connect_db(app)
with app.app_context():
    db.create_all()


@app.route('/')
def root():
    '''Render homepage'''
    return render_template('index.html')

@app.route('/api/cupcakes')
def cupcake_list():
    '''Return a list of the cupcakes'''
    cupcakes = [cupcake.to_dict() for cupcake in Cupcake.query.all()]
    return jsonify(cupcakes=cupcakes)

@app.route('/api/cupcakes', methods=['POST'])
def add_cupcake():
    '''Add cupcake to list, and return data for that cupcake'''

    data = request.json
    cupcake = Cupcake(flavor = data['flavor'], size = data['size'], rating = data['rating'], image = data['image'] or None)

    db.session.add(cupcake)
    db.session.commit()
    return (jsonify(cupcake=cupcake.to_dict()), 201)

@app.route('/api/cupcakes/<int:cupcake_id>')
def get_cupcake(cupcake_id):
    '''Return info on a specified cupcake'''
    cupcake = Cupcake.query.get_or_404(cupcake_id)
    return jsonify(cupcake=cupcake.to_dict())

@app.route('/api/cupcakes/<int:cupcake_id>', methods=['PATCH'])
def update_cupcake(cupcake_id):
    '''Update cupcake in list with new info then return that new data'''
    data = request.json
    cupcake = Cupcake.query.get_or_404(cupcake_id)

    cupcake.flavor = data['flavor']
    cupcake.size = data['size']
    cupcake.rating = data['rating']
    cupcake.image = data['image']

    db.session.add(cupcake)
    db.session.commit()
    return jsonify(cupcake=cupcake.to_dict())

@app.route('/api/cupcakes/<int:cupcake_id>', methods=['DELETE'])
def delete_cupcake(cupcake_id):
    '''Delete cupcake from list'''
    cupcake = Cupcake.query.get_or_404(cupcake_id)

    db.session.delete(cupcake)
    db.session.commit()
    return jsonify(msg='Deleted')