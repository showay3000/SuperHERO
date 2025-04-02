# Import required Flask modules and extensions
from flask import Flask, request, jsonify
from flask_migrate import Migrate
from models import db, Hero, Power, HeroPower

# Initialize Flask application
app = Flask(__name__)

# Configure database URI and disable modification tracking
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQLAlchemy with Flask app
db.init_app(app)

# Initialize Flask-Migrate for database migrations
migrate = Migrate(app, db)

# Route for home page
@app.route('/')
def home():
    return 'Superheroes API'

# GET /heroes - Retrieve all heroes
@app.route('/heroes', methods=['GET'])
def get_heroes():
    # Query all heroes from database
    heroes = Hero.query.all()
    
    # Format heroes data into dictionary list
    heroes_data = [{
        "id": hero.id, 
        "name": hero.name, 
        "super_name": hero.super_name
    } for hero in heroes]
    
    # Return JSON response
    return jsonify(heroes_data)

# GET /heroes/:id - Retrieve a specific hero by ID
@app.route('/heroes/<int:id>', methods=['GET'])
def get_hero(id):
    # Find hero by ID
    hero = Hero.query.get(id)
    
    # Return 404 if hero not found
    if not hero:
        return jsonify({"error": "Hero not found"}), 404
    
    # Build list of hero's powers with details
    hero_powers = []
    for hp in hero.hero_powers:
        hero_powers.append({
            "id": hp.id,
            "hero_id": hp.hero_id,
            "power_id": hp.power_id,
            "strength": hp.strength,
            "power": {
                "id": hp.power.id,
                "name": hp.power.name,
                "description": hp.power.description
            }
        })
    
    # Format complete hero data
    hero_data = {
        "id": hero.id,
        "name": hero.name,
        "super_name": hero.super_name,
        "hero_powers": hero_powers
    }
    
    return jsonify(hero_data)

# GET /powers - Retrieve all powers
@app.route('/powers', methods=['GET'])
def get_powers():
    # Query all powers from database
    powers = Power.query.all()
    
    # Format powers data into dictionary list
    powers_data = [{
        "id": power.id, 
        "name": power.name, 
        "description": power.description
    } for power in powers]
    
    return jsonify(powers_data)

# GET /powers/:id - Retrieve a specific power by ID
@app.route('/powers/<int:id>', methods=['GET'])
def get_power(id):
    # Find power by ID
    power = Power.query.get(id)
    
    # Return 404 if power not found
    if not power:
        return jsonify({"error": "Power not found"}), 404
    
    # Format power data
    power_data = {
        "id": power.id,
        "name": power.name,
        "description": power.description
    }
    
    return jsonify(power_data)

# PATCH /powers/:id - Update a power's description
@app.route('/powers/<int:id>', methods=['PATCH'])
def update_power(id):
    # Find power by ID
    power = Power.query.get(id)
    
    # Return 404 if power not found
    if not power:
        return jsonify({"error": "Power not found"}), 404
    
    # Get JSON data from request
    data = request.get_json()
    
    try:
        # Update description if provided
        if 'description' in data:
            power.description = data['description']
            db.session.commit()
            
            # Return updated power data
            return jsonify({
                "id": power.id,
                "name": power.name,
                "description": power.description
            })
    except Exception as e:
        # Rollback on error and return 400
        db.session.rollback()
        return jsonify({"errors": ["validation errors"]}), 400

# POST /hero_powers - Create a new hero-power association
@app.route('/hero_powers', methods=['POST'])
def create_hero_power():
    # Get JSON data from request
    data = request.get_json()
    
    try:
        # Create new HeroPower instance
        hero_power = HeroPower(
            strength=data['strength'],
            power_id=data['power_id'],
            hero_id=data['hero_id']
        )
        
        # Add to session and commit
        db.session.add(hero_power)
        db.session.commit()
        
        # Get related hero and power for response
        hero = Hero.query.get(data['hero_id'])
        power = Power.query.get(data['power_id'])
        
        # Return created hero-power with details
        return jsonify({
            "id": hero_power.id,
            "hero_id": hero_power.hero_id,
            "power_id": hero_power.power_id,
            "strength": hero_power.strength,
            "hero": {
                "id": hero.id,
                "name": hero.name,
                "super_name": hero.super_name
            },
            "power": {
                "id": power.id,
                "name": power.name,
                "description": power.description
            }
        }), 201  # 201 Created status code
    except Exception as e:
        # Rollback on error and return 400
        db.session.rollback()
        return jsonify({"errors": ["validation errors"]}), 400

# Run the application if executed directly
if __name__ == '__main__':
    app.run(port=5555)