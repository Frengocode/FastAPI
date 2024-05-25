from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ..database import get_db
from .. import schemas, models
from .oauts2 import get_current_user
from ..hashing import pwd_cxt, Hash


router = APIRouter(
    tags=['user'],
    prefix='/user'
)

@router.get('/{id}', response_model=schemas.ShowUser)
async def user_detail(id, db:Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return user



@router.post('/', tags=['users'])
def create_user(request: schemas.User, db: Session = Depends(get_db)):
    existing_user = db.query(models.User).filter(models.User.name == request.name).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="This username is already in use"
        )

    
    hashed_password = Hash.bcrypt(request.password) 
    new_user = models.User(
        name=request.name,
        email=request.email,
        password=hashed_password
    )

    if not new_user.email.endswith('@gmail.com'):

        raise HTTPException(detail='Ошибка', status_code=402)
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user