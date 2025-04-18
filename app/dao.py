from datetime import date, timedelta
from sqlalchemy import func
from sqlalchemy.exc import SQLAlchemyError
from app import db
from app.models import User, File, StoragePurchase


### Email-----------------------------------------------------------------------------
def is_email_exist(email):
    return User.query.filter(User.email.__eq__(email)).first() is not None


### User-----------------------------------------------------------------------------
def add_user(name, email, password):
    try:
        new_user = User(name=name, email=email, password=password)
        db.session.add(new_user)
        db.session.commit()
        return True
    except SQLAlchemyError:
        return False


def user_auth(email, password):
    user = User.query.filter(User.email.__eq__(email), User.password.__eq__(password)).first()

    if user:
        return user


def get_user_by_id(user_id):
    return User.query.get(user_id)


### File-----------------------------------------------------------------------------
def get_file_by_id(file_id):
    return File.query.get(file_id)


def add_file(file_name, file_path, file_size, file_type, user_id):
    try:
        file = File(file_name=file_name, file_path=file_path, file_size=file_size, file_type=file_type, user_id=user_id)
        db.session.add(file)
        db.session.commit()
        return True
    except SQLAlchemyError:
        return False


def is_file_exist(file_name, user_id):
    return File.query.filter(File.user_id.__eq__(user_id), File.file_name.__eq__(file_name)).first() is not None


def load_user_files(user_id, file_type=None, name=None):
    files = File.query.filter(File.user_id.__eq__(user_id))

    if file_type:
        files = files.filter(File.file_type.__eq__(file_type))

    if name:
        files = files.filter(File.file_name.contains(name))

    return files.all()


def delete_file(file_id):
    try:
        file = get_file_by_id(file_id=file_id)
        db.session.delete(file)
        db.session.commit()
        return True
    except SQLAlchemyError:
        return False


def rename_file(file_id, new_file_name, new_file_path):
    try:
        file = get_file_by_id(file_id=file_id)
        file.file_name = new_file_name
        file.file_path = new_file_path
        db.session.commit()
        return True
    except SQLAlchemyError:
        return False

def get_all_file_type():
    return db.session.query(File.file_type).distinct().all()


### Storage-----------------------------------------------------------------------------
def get_total_storage_used(user_id):
    result = db.session.query(func.sum(File.file_size)).filter(File.user_id == user_id).scalar()

    return result


def get_total_storage(user_id):
    result = db.session.query(func.sum(StoragePurchase.size)).filter(StoragePurchase.user_id == user_id).scalar() or 0
    user = get_user_by_id(user_id)
    default_storage = user.default_storage if user else 0

    return result + default_storage


### Storage purchase---------------------------------------------------------------------------------
def get_storage_purchase(sp_id):
    return StoragePurchase.query.get(sp_id)


def add_storage_purchase(user_id,size,price):
    today = date.today()
    expiry_day = today + timedelta(days=30)

    try:
        purchase = StoragePurchase(user_id=user_id,size=size,price=price,expiry_date=expiry_day)
        db.session.add(purchase)
        db.session.commit()
        return True
    except SQLAlchemyError:
        return False

def success_payment(sp_id):
    sp = get_storage_purchase(sp_id=sp_id)
    try:
        sp.status = True
        db.session.commit()
    except SQLAlchemyError:
        return False

### History payment -----------------------------------------------------------------------------------------
def get_history_payment(user_id):
    return StoragePurchase.query.filter(StoragePurchase.user_id.__eq__(user_id)).order_by(StoragePurchase.pay_date.desc()).all()