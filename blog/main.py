from fastapi import FastAPI, Depends, status, Response, HTTPException
from .schemas import Blog
from . import schemas, models, database
from sqlalchemy.orm import Session
from typing import List
from .hashing import Hash
app = FastAPI()

models.Base.metadata.create_all(database.engine)


def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/blog", status_code=status.HTTP_201_CREATED, tags=["Blogs"])
def create(request: Blog, db: Session = Depends(get_db)):
    new_blog = models.Blog(title=request.title, body=request.body)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog


@app.get("/blog",response_model=List[schemas.ShowBlog], tags=["Blogs"])
async def all_blogs(db: Session = Depends(get_db)):
    blogs = db.query(models.Blog).all()
    return blogs


@app.get("/blog/{blog_id}", status_code=200, response_model=schemas.ShowBlog, tags=["Blogs"])
async def single_blog(blog_id, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == blog_id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with {blog_id} not found")
    return blog


@app.delete("/blog/{blog_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Blogs"])
async def delete_blog(blog_id, db: Session = Depends(get_db)):
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


@app.put("/blog/{blog_id}", status_code=status.HTTP_200_OK, tags=["Blogs"])
async def blog_update(blog_id, request: schemas.Blog, db: Session = Depends(get_db)):
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


@app.post("/user", response_model=schemas.ShowUser, tags=["Users"])
async def crate_user(request: schemas.User, db: Session = Depends(get_db)):

    new_user = models.User(name=request.name, email=request.email, password=Hash.bcrypt(request.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@app.get("/user/{user_id}", response_model=schemas.ShowUser, tags=["Users"])
async def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User not found!")
    return user
