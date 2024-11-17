from fastapi import FastAPI, Request, status
from .routers import auth, todos, admin, users

# from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

from fastapi.responses import RedirectResponse

from .models import Base

from .database import engine

app = FastAPI()

Base.metadata.create_all(bind=engine)

# templates = Jinja2Templates(directory="TodoApp/templates")


app.mount("/static", StaticFiles(directory="TodoApp/static"), name="static")


@app.get("/")
def test(request: Request):
    # return templates.TemplateResponse("home.html", {"request": request})
    return RedirectResponse(url="/todos/todo-page", status_code=status.HTTP_302_FOUND)


@app.get("/healthy")
def health_check():
    return {"status": "Healthy"}


app.include_router(users.router)
app.include_router(auth.router)
app.include_router(todos.router)
app.include_router(admin.router)
