from flask_sqlalchemy import SQLAlchemy

db=SQLAlchemy()

class Order(db.Model):
    __tablename__="orders"
    _id = db.Column("id",db.Integer,primary_key=True,autoincrement=True)
    user_id = db.Column(db.Integer, nullable=False)
    number_of_items = db.Column(db.Integer, nullable=False)
    total_amount = db.Column(db.Numeric(10, 2), nullable=False)
    
    def __init__(self,user_id,number_of_items,total_amount):
        self.user_id=user_id
        self.number_of_items=number_of_items
        self.total_amount=total_amount