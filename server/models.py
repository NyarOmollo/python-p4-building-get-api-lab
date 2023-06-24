from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy_serializer import SerializerMixin
metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})
db = SQLAlchemy(metadata=metadata)
class Bakery(db.Model, SerializerMixin):
    __tablename__ = 'bakeries'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String())
    baked_goods = db.relationship('BakedGood', backref='bakery')
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())
    
    def __repr__ (self):
        return f'<Bakery {self.name}>'
    

class BakedGood(db.Model, SerializerMixin):
    __tablename__ = 'baked_goods'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    price = db.Column(db.Integer)
    bakery_id = db.Column(db.Integer, db.ForeignKey('bakeries.id'))
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    def __repr__ (self):
        return f'<BakedGood {self.name} for {self.price}>'