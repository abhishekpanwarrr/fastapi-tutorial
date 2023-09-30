from fastapi import APIRouter, HTTPException, status, Depends
from .. import schemas, models, database
from sqlalchemy.orm import Session
from typing import List
from ..oauth2 import get_current_user

router = APIRouter(tags=["Blogs"], prefix="/blog")


@router.post("/", status_code=status.HTTP_201_CREATED)
def create(request: schemas.Blog, db: Session = Depends(database.get_db)):
    new_blog = models.Blog(title=request.title, body=request.body, user_id=1)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog


@router.get("/", response_model=List[schemas.ShowBlog])
async def all_blogs(db: Session = Depends(database.get_db), current_user: schemas.User = Depends(get_current_user)):
    blogs = db.query(models.Blog).all()
    return blogs


@router.get("/{blog_id}", status_code=200, response_model=schemas.ShowBlog)
async def single_blog(blog_id, db: Session = Depends(database.get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == blog_id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with {blog_id} not found")
    return blog


@router.delete("/{blog_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_blog(blog_id, db: Session = Depends(database.get_db)):
    try:
        blog = db.query(models.Blog).filter(models.Blog.id == blog_id)
        if not blog.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with id {blog_id} not found")
        blog.delete(synchronize_session=False)
        db.commit()
        return 'Done'
    except:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Something went wrong. Please "
                                                                                      "try again")


@router.put("/{blog_id}", status_code=status.HTTP_200_OK)
async def blog_update(blog_id, request: schemas.Blog, db: Session = Depends(database.get_db)):
    try:
        blog = db.query(models.Blog).filter(models.Blog.id == blog_id)
        if not blog.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with id {blog_id} not found")
        blog.update({'title': request.title, 'body': request.body})
        db.commit()
        return {"message": f"Blog with id {blog_id} updated successfully."}
    except:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Something went wrong. Please "
                                                                                      "try again")
