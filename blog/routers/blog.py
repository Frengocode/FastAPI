from fastapi import APIRouter, Depends, Response, HTTPException, status
from sqlalchemy.orm import Session
from .. import schemas, models
from ..database import get_db
from .oauts2 import get_current_user

router = APIRouter(
    tags=['blogs'],
    prefix='/blog'
)


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.Blog)
async def create_blog(
    request: schemas.Blog,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_user)
):
    db_user = db.query(models.User).filter(models.User.id == current_user.id).first()
    
    new_blog = models.Blog(
        title=request.title,
        body=request.body,
        creator_id=db_user.id 
    )
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    
    response_blog = schemas.Blog(
        title=new_blog.title,
        body=new_blog.body,
        creator_name=db_user.name  
    )
    return response_blog


@router.get('/{id}', tags=['blogs'], response_model=schemas.Blog)
async def show_blog(id: int, response: Response, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(status_code=404, detail="Blog not found")

    blog_creator_name = blog.creator.name

    blog_with_creator_name = schemas.Blog(
        title=blog.title,
        body=blog.body,
        creator_name=blog_creator_name
    )
    return blog_with_creator_name





@router.delete('/{id}', tags=['blogs'], status_code=status.HTTP_200_OK)
def destroy(id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Blog not found")
    
    if blog.creator_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to delete this blog")
    
    db.delete(blog)
    db.commit()
    return {"detail": "Blog deleted successfully"}



@router.put('/{id}', status_code=status.HTTP_200_OK, tags=['blogs'])
async def update_blog(id: int, request: schemas.Blog, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)): 
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Blog not found")
    
    if blog.creator_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to update this blog")
    
    blog.title = request.title
    blog.body = request.body
    db.commit()
    return {"detail": "Blog updated successfully"}