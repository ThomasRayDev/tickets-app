from fastapi import Security, Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from jose import jwt, JWTError
from database import get_db
from models import User


SECRET_KEY = 'secret_key_example'
ALGORITHM = 'HS256'

security = HTTPBearer()


# def get_current_user(credentials: HTTPAuthorizationCredentials = Security(security)):
#   try:
#     token = credentials.credentials
#     payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#     login = payload.get('sub')
#     if login is None:
#       raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid token')
#     return login
#   except JWTError:
#     raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid token')

def get_current_user(credentials: HTTPAuthorizationCredentials = Security(security), db: Session = Depends(get_db)):
  try:
    token = credentials.credentials
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    login = payload.get('sub')
    if login is None:
      raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid token')
    return db.query(User).filter(User.login == login).first()
  except JWTError:
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail='Invalid token')
  