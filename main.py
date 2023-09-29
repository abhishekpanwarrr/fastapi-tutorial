from fastapi import FastAPI
from typing import Optional
from pydantic import BaseModel


app = FastAPI()


@app.get("/blog")
async def get_err(limit=10, published: bool = False, sort: Optional[str]= None):
    if published:
        return {"published": "Its published blogs"}
    return {"author": f"Abhishek Panwar - {limit} and published is {published}"}


@app.get("/blog/{blog_id}")
async def about(blog_id: int):
    return {"Blog id is": blog_id}


class Blog(BaseModel):
    title: str
    body: str
    published: Optional[bool] = False


@app.post("/blog")
async def create_blog(req: Blog):
    return {"data": f"blog with title- {req.title}"}

