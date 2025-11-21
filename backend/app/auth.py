from dotenv import load_dotenv
import os
from datetime import datetime, timedelta, timezone
from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer
import jwt
from bcrypt import hashpw, gensalt, checkpw
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.db import get_async_session, User
from app.schemas import TokenData, UserInDB

load_dotenv()
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")
ALGORITHM = 'HS256'

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")

def get_hashed_password(password: str):
  return hashpw(password.encode("utf-8"), gensalt()).decode("utf-8")

def verify_password(hashed_password: str, password: str):
  try:
    return checkpw(hashed_password.encode("utf-8"), password.encode("utf-8"))
  except:
    return False
  
async def get_user_by_email(email: str, session: AsyncSession):
  result = await session.execute(select(User).where(User.email==email))
  return result.scalar_one_or_none()
  
def authenticate_user(email: str, password: str, session: AsyncSession = Depends(get_async_session)):
  user = get_user_by_email(email, session)
  if not user:
    return False
  if not verify_password(user.password, password):
    return False
  
  return user

def create_access_token(data: dict, expires_delta: timedelta | None = None):
  to_encode = data.copy()
  if expires_delta:
    expire = datetime.now(timezone.utc) + expires_delta
  else:
    expire = datetime.now(timezone.utc) + timedelta(minutes=60)
  
  to_encode.update({"exp": expire})
  encoded_jwt = jwt.encode(to_encode, JWT_SECRET_KEY, algorithm=ALGORITHM)

  return encoded_jwt

async def get_current_user(token: str = Depends(oauth2_scheme), session: AsyncSession = Depends(get_async_session)):
  credential_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials", headers={"WWW-Authenticate": "Bearer"})
  try:
    payload = jwt.decode(token, JWT_SECRET_KEY, alogirthm=ALGORITHM)
    email = payload.get('sub')
    if email is None:
      raise credential_exception
    token_data = TokenData(email=email)
  except:
    raise credential_exception
  
  user = await get_user_by_email(email, session)
  if user is None:
    raise credential_exception
  
  return user

async def get_current_active_user(current_user: UserInDB = Depends(get_current_user)):
  if current_user.disabled:
    raise HTTPException(status_code=400, detail="Inactive User", headers={"WWW-Authenticate": "Bearer"})
  
async def require_role(required_role: str):
  def role_checker(user: dict = Depends(get_current_active_user)):
    if user["role"] != required_role:
      raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not enough permissions")
    
  return role_checker

  
