from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Hero(db.Model):
    __tablename__ = 'heroes'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    super_name = db.Column(db.String(50), nullable=False)
    
    hero_powers = db.relationship('HeroPower', backref='hero', cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Hero {self.name}, {self.super_name}>'

class Power(db.Model):
    __tablename__ = 'powers'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(255), nullable=False)
    
    hero_powers = db.relationship('HeroPower', backref='power', cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Power {self.name}>'

class HeroPower(db.Model):
    __tablename__ = 'hero_powers'

    id = db.Column(db.Integer, primary_key=True)
    strength = db.Column(db.String(20), nullable=False)
    hero_id = db.Column(db.Integer, db.ForeignKey('heroes.id'), nullable=False)
    power_id = db.Column(db.Integer, db.ForeignKey('powers.id'), nullable=False)

    __table_args__ = (
        db.CheckConstraint(
            "strength IN ('Strong', 'Weak', 'Average')", 
            name='check_strength_values'
        ),
    )

    def __repr__(self):
        return f'<HeroPower hero_id={self.hero_id}, power_id={self.power_id}>'