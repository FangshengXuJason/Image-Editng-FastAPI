import pathlib
import os
import io
from fastapi import(
    FastAPI,
    Request
    )
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

BASE_DIR = pathlib.Path(__file__).parent
# UPLOAD_DIR = BASE_DIR / "uploads"

print(BASE_DIR / "templates")

app = FastAPI()
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

@app.get("/", response_class=HTMLResponse) # http GET -> JSON
def home_view(request: Request):
    print(request)
    # can use string substitution
    return templates.TemplateResponse("home.html", {"request": request, "abc": 123})