from app import app, db
from sqlalchemy import Column, String, Integer, ForeignKey, Date, Float, func
from sqlalchemy.orm import relationship, backref
from flask_login import UserMixin


class User(db.Model, UserMixin):
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    password = Column(String(255), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    default_storage = Column(Integer, default=100, nullable=True)
    files = relationship('File',backref='user', lazy=True, passive_deletes=True)
    storage_purchase = relationship('StoragePurchase', backref='user', lazy=True, passive_deletes=True)

    def __str__(self):
        return self.name


class File(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    file_name = Column(String(255), nullable=False)
    file_path = Column(db.String(500), nullable=False)
    upload_date = Column(Date, default=db.func.current_timestamp())
    file_size = Column(Float, nullable=False)
    file_type = Column(String(50), nullable=False)
    user_id = Column(Integer, ForeignKey(User.id, ondelete="CASCADE"), nullable=False)

    def __str__(self):
        return self.file_name

class StoragePurchase(db.Model):
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey(User.id, ondelete="CASCADE"), nullable=False)
    size = db.Column(db.Integer, nullable=False)
    price = Column(Float, default=0,nullable=False)
    pay_date = Column(Date, default=func.current_timestamp(), nullable=False)
    expiry_date = Column(Date, default=func.current_timestamp(), nullable=False)


if __name__ == "__main__":
    with app.app_context():
        db.create_all()

        user1 = User(name="Con Meo",email='123@gmail.com',password='123')
        user2 = User(name="Con Cho", email='456@gmail.com', password='456')
        db.session.add_all([user1,user2])
        db.session.commit()