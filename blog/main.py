from fastapi import FastAPI
from .routers import blog, authentication, user


app = FastAPI()

app.include_router(blog.router)
app.include_router(authentication.router)
app.include_router(user.router)






