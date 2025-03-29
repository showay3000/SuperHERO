from flask import Flask, request, jsonify
from flask_migrate import Migrate
from models import db, Hero, Power, HeroPower

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
migrate = Migrate(app, db)

@app.route('/')
def home():
    return 'Superheroes API'

# GET /Heroes
@app.route('/heroes', methods=['GET'])
def get_heroes():
    heroes = Hero.query.all()
    heroes_data = [{"id": hero.id, "name": hero.name, "super_name": hero.super_name} for hero in heroes]
    return jsonify(heroes_data)

# GET /Heroes:id
@app.route('/heroes/<int:id>', methods=['GET'])
def get_hero(id):
    hero = Hero.query.get(id)
    if not hero:
        return jsonify({"error": "Hero not found"}), 404
    
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
    
    hero_data = {
        "id": hero.id,
        "name": hero.name,
        "super_name": hero.super_name,
        "hero_powers": hero_powers
    }
    return jsonify(hero_data)

# GET /powers
@app.route('/powers', methods=['GET'])
def get_powers():
    powers = Power.query.all()
    powers_data = [{"id": power.id, "name": power.name, "description": power.description} for power in powers]
    return jsonify(powers_data)

# GET /powers/:id
@app.route('/powers/<int:id>', methods=['GET'])
def get_power(id):
    power = Power.query.get(id)
    if not power:
        return jsonify({"error": "Power not found"}), 404
    power_data = {
        "id": power.id,
        "name": power.name,
        "description": power.description
    }
    return jsonify(power_data)

# PATCH /powers/:id
@app.route('/powers/<int:id>', methods=['PATCH'])
def update_power(id):
    power = Power.query.get(id)
    if not power:
        return jsonify({"error": "Power not found"}), 404
    
    data = request.get_json()
    try:
        if 'description' in data:
            power.description = data['description']
            db.session.commit()
            return jsonify({
                "id": power.id,
                "name": power.name,
                "description": power.description
            })
    except Exception as e:
        db.session.rollback()
        return jsonify({"errors": ["validation errors"]}), 400

# POST /hero_powers
@app.route('/hero_powers', methods=['POST'])
def create_hero_power():
    data = request.get_json()
    
    try:
        hero_power = HeroPower(
            strength=data['strength'],
            power_id=data['power_id'],
            hero_id=data['hero_id']
        )
        db.session.add(hero_power)
        db.session.commit()
        
        hero = Hero.query.get(data['hero_id'])
        power = Power.query.get(data['power_id'])
        
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
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"errors": ["validation errors"]}), 400

if __name__ == '__main__':
    app.run(port=5555)