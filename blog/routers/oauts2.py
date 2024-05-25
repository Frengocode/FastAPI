from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from ..token import SECRET_KEY, TokenData, ALGORITHM, verify_token, TokenData
from .. import schemas, models
from ..database import get_db, SessionLocal
from sqlalchemy.orm import Session


oauth2_schema = OAuth2PasswordBearer(tokenUrl='login')


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

async def get_current_user(token: str = Depends(oauth2_schema), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        name: str = payload.get("sub")
        if name is None:
            raise credentials_exception
        token_data = TokenData(name=name)
    except JWTError:
        raise credentials_exception
    user = db.query(models.User).filter(models.User.name == name).first()
    if user is None:
        raise credentials_exception
    return user
