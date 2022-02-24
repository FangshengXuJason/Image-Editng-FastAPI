from curses import noecho
import pathlib
import os
import io
from typing import Optional, Tuple
import uuid
from functools import lru_cache
from fastapi import(
    FastAPI,
    Header,
    HTTPException,
    Depends,
    Request,
    File,
    UploadFile
    )
import pytesseract
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseSettings, BaseModel
from PIL import Image
from typing import List, Tuple
class Settings(BaseSettings):
    app_auth_token: str
    debug: bool = False
    echo_active: bool = False
    app_auth_token_prod: str = None
    skip_auth: bool = False

    class Config:
        env_file = ".env"

@lru_cache
def get_settings():
    return Settings()

settings = get_settings()
DEBUG=settings.debug

BASE_DIR = pathlib.Path(__file__).parent
UPLOAD_DIR = BASE_DIR / "uploads"

# param for each image editing operation 
class ImgEditParam(BaseModel): 
    name: str = "no_operation"
    toggle: Optional[bool] = False
    width: int = 0
    length: int = 0

app = FastAPI()
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

@app.get("/", response_class=HTMLResponse) # http GET -> JSON
def home_view(request: Request, settings:Settings = Depends(get_settings)):
    return templates.TemplateResponse("home.html", {"request": request, "author": "FangshengXu"})

def flip(original: Image, top_bottem: bool = True) -> Image: 
    if top_bottem: 
        result = original.transpose(Image.FLIP_TOP_BOTTOM)
    else: 
        result = original.transpose(Image.FLIP_LEFT_RIGHT)
    return result

@app.post("/flip/", response_class=FileResponse) # flip the image horizontally or vertically
async def flip_view(file:UploadFile = File(...), settings:Settings = Depends(get_settings)):
    bytes_str = io.BytesIO(await file.read())
    try:
        img = Image.open(bytes_str)
    except:
        raise HTTPException(detail="Invalid image", status_code=400)
    
    new_img = flip(img)
    fname = pathlib.Path(file.filename)
    fext = fname.suffix # .jpg, .txt
    dest = UPLOAD_DIR / f"{uuid.uuid1()}{fext}"
    new_img.save(dest)
    return dest 
    
def greyscale(original: Image) -> Image: 
    return  original.convert('L')

@app.post("/greyscale/", response_class=FileResponse) # flip the image horizontally or vertically
async def greyscale_view(file:UploadFile = File(...), settings:Settings = Depends(get_settings)):
    bytes_str = io.BytesIO(await file.read())
    try:
        img = Image.open(bytes_str)
    except:
        raise HTTPException(detail="Invalid image", status_code=400)

    new_img = greyscale(img)
    fname = pathlib.Path(file.filename)
    fext = fname.suffix # .jpg, .txt
    dest = UPLOAD_DIR / f"{uuid.uuid1()}{fext}"
    new_img.save(dest)
    return dest 

from enum import Enum

class operationName(str, Enum):
    flip = "flip"
    greyscale = "greyscale"
    resize = "resize"
    rotate = "rotate"
    thumbnail = "thumbnail"

@app.post("/api/v1/")
async def edit_multiple_images(operations: List[ImgEditParam]):
    for operation in operations: 
        print(operation.name)
    return operations