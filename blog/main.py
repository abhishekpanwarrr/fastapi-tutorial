from fastapi import FastAPI, Depends, status, Response, HTTPException
from .schemas import Blog
from . import schemas, models, database
from sqlalchemy.orm import Session

app = FastAPI()

models.Base.metadata.create_all(database.engine)


def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/blog", status_code=status.HTTP_201_CREATED)
def create(request: Blog, db: Session = Depends(get_db)):
    new_blog = models.Blog(title=request.title, body=request.body)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog


@app.get("/blog")
async def all_blogs(db: Session = Depends(get_db)):
    blogs = db.query(models.Blog).all()
    return blogs


@app.get("/blog/{blog_id}", status_code=200)
async def single_blog(blog_id, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == blog_id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Blog with {blog_id} not found")
    return blog


@app.delete("/blog/{blog_id}", status_code=status.HTTP_204_NO_CONTENT)
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


@app.put("/blog/{blog_id}", status_code=status.HTTP_200_OK)
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
