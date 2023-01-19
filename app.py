"""Flask app for Cupcakes"""
from flask import Flask, jsonify, request, render_template, redirect
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, Cupcake, default_image

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///cupcakes'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = 'AdoptDontShop'
app.config['DEBUG_TB_INTERCEPT-REDIRECTS'] = False
# app.run(debug=True)
debug = DebugToolbarExtension(app)

app.app_context().push()

connect_db(app)
db.create_all()

##################### FLASK ROUTES ####################
@app.route('/')
def render_home_age():
    return render_template('home.html', cupcakes=Cupcake.query.all())

##################### API ROUTES ######################

@app.route('/api/cupcakes')
def list_cupcakes():
    '''Query the cupcake model for all instances of cupcakes, then we serialize
    and return json list of all cupcakes and their attributes'''
    return jsonify(cupcakes=[cupcake.serialize() for cupcake in Cupcake.query.all()])

@app.route('/api/cupcakes/<int:cupcake_id>')
def get_cupcake(cupcake_id):
    '''Query the cupcake model for specific instance of cupcake by cupcake id, 
    then we serialize and return json of this cupcake and it's attributes'''
    return jsonify(cupcake=Cupcake.query.get_or_404(cupcake_id).serialize())

@app.route('/api/cupcakes', methods=['POST'])
def create_cupcake():
    '''Create new cupcake based off of HTTP request. Check that the flavor, size, and rating
    all have values. If image is an empty string, we set it equal to default image. Then we create
    our new cupcake and commit it to the database'''
    if (request.json['flavor'] != None and request.json['size'] != None 
            and request.json['rating'] != None):
        
        if request.json['image'] == '':
            request.json['image'] = default_image

        new_cupcake = Cupcake(flavor=request.json.get('flavor'), size=request.json.get('size'), 
                rating=request.json.get('rating'), image=request.json.get('image'))
        
        db.session.add(new_cupcake)
        db.session.commit()

    return (jsonify(cupcake=new_cupcake.serialize()), 201)

@app.route('/api/cupcakes/<int:cupcake_id>', methods=['PATCH'])
def update_cupcake(cupcake_id):
    '''Query the cupcake model for specific instance of cupcake busing cupcake id, 
    then update attributes if they've changed. Then return json this cupcake 
    and it's attributes'''
    cupcake = Cupcake.query.get_or_404(cupcake_id)
    cupcake.update(request.json)

    db.session.add(cupcake)
    db.session.commit()

    return jsonify(cupcake=Cupcake.query.get_or_404(cupcake_id).serialize())

@app.route('/api/cupcakes/<cupcake_id>', methods=['DELETE'])
def delete_cupcake(cupcake_id):
    '''Query the cupcake model for specific instance of cupcake using cupcake id, 
    then delete cupcake :( Return json message that deletion was successful'''
    cupcake = Cupcake.query.get_or_404(cupcake_id)

    db.session.delete(cupcake)
    db.session.commit()

    return jsonify(message=f"Cupcake {cupcake.id} deleted")
