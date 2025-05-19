from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from models import User
from database import get_db
from dependencies import get_current_user
from schemas import UserCreate, UserLogin, ChangePasswordSchema, UserOutSchema
from jose import jwt
from datetime import datetime, timedelta


SECRET_KEY = 'secret_key_example'
ALGORITHM = 'HS256'
ACCESS_TOKEN_EXPIRE_MINUTES = 60

router = APIRouter()


pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


def get_password_hash(password):
  return pwd_context.hash(password)

def verify_password(plain_password, hash_password):
  return pwd_context.verify(plain_password, hash_password)

def create_access_token(data: dict, expires_delta: timedelta = None):
  to_encode = data.copy()
  expire = datetime.utcnow() + (expires_delta or timedelta(minutes=60))
  to_encode.update({'exp': expire})
  return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


@router.post('/register', tags=['Auth'], response_model = UserOutSchema)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
  if db.query(User).filter(User.login == user.login).first():
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='User already registered')
  hashed_password = get_password_hash(user.password)
  db_user = User(login=user.login, hashed_password=hashed_password, firstname=user.firstname, secondname=user.secondname)
  db.add(db_user)
  db.commit()
  db.refresh(db_user)
  return db_user

@router.post('/login', tags=['Auth'])
def login(user: UserLogin, db: Session = Depends(get_db)):
  db_user = db.query(User).filter(User.login == user.login).first()
  if not db_user or not verify_password(user.password, db_user.hashed_password):
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid credentials')
  
  access_token = create_access_token({'sub': db_user.login})
  return { "auth": { "access_token": access_token, "token_type": "bearer" }, "success": True }

@router.get('/current-user', tags=['Auth'], response_model = UserOutSchema)
def return_current_user(user = Depends(get_current_user)):
  return user

@router.post('/change-password', tags=['Auth'], response_model = UserOutSchema)
def change_password(password_schema: ChangePasswordSchema, db_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
  if not verify_password(password_schema.old_password, db_user.hashed_password):
    raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Incorrect password')
  if password_schema.old_password == password_schema.new_password:
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Password cannot be reused')
  hashed_password = get_password_hash(password_schema.new_password)
  db_user.hashed_password = hashed_password
  db.commit()
  db.refresh(db_user)
  return db_user
