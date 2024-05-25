from fastapi import FastAPI
from typing import Any, Optional
from pydantic import BaseModel


app = FastAPI()

@app.get('/')
async def home():
    return   {'data': {'name': 'Bob'} }





class Blog(BaseModel):
    title: str
    body: str
    published: Optional[bool]


@app.post('/blog')
async def add_blog(request: Blog):
    return {'data': f'Blog Is Created with title {request.title} '}