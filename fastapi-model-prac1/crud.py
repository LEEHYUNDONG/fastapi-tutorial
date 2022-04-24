from sqlalchemy.orm import Session
import model, schemas
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"])

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def get_user(db:Session, user_id:int):
    return db.query(model.User).filter(model.User.id == user_id).first()

def get_user_by_email(db : Session, email : str):
    return db.query(model.User).filter(model.User.email == email).first()

def get_users(db:Session, skip:int = 0, limit : int= 100):
    return db.query(model.User).offset(skip).limit(limit).all()

def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = get_password_hash(user.password)
    db_user = model.User(email=user.email, password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user