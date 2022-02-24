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
TEMP_DIR = BASE_DIR / "temps"

# param for each image editing operation 
class ImgEditParam(BaseModel): 
    name: str = "no_operation"
    toggle: Optional[bool] = False
    width: int = 0
    length: int = 0

app = FastAPI()
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

@app.get("/", response_class=HTMLResponse) # http GET -> JSON
def home_view(request: Request):
    return templates.TemplateResponse("home.html", {"request": request, "author": "FangshengXu"})


def flip(img: Image, top_bottem: bool) -> Image: 
    if top_bottem: 
        return img.transpose(Image.FLIP_TOP_BOTTOM)
    else: 
        return img.transpose(Image.FLIP_LEFT_RIGHT)

@app.post("/flip/", response_class=FileResponse) # flip the image horizontally or vertically
async def flip_view(top_bottem: bool = True, file:UploadFile = File(...)):
    bytes_str = io.BytesIO(await file.read())
    try:
        img = Image.open(bytes_str)
    except:
        raise HTTPException(detail="Invalid image", status_code=400) 
    img = flip(img, top_bottem)
    fname = pathlib.Path(file.filename)
    fext = fname.suffix # .jpg, .txt
    dest = UPLOAD_DIR / f"{uuid.uuid1()}{fext}"
    img.save(dest)
    return dest 
    
def greyscale(img: Image) -> Image: 
    return  img.convert('L')

@app.post("/greyscale/", response_class=FileResponse) # flip the image horizontally or vertically
async def greyscale_view(file:UploadFile = File(...)):
    bytes_str = io.BytesIO(await file.read())
    try:
        img = Image.open(bytes_str)
    except:
        raise HTTPException(detail="Invalid image", status_code=400)

    img = greyscale(img)
    fname = pathlib.Path(file.filename)
    fext = fname.suffix # .jpg, .txt
    dest = UPLOAD_DIR / f"{uuid.uuid1()}{fext}"
    img.save(dest)
    return dest 

def resize(img: Image, size: Tuple[int, int]) -> Image: 
    return img.resize(size)

@app.post("/resize/", response_class=FileResponse) # flip the image horizontally or vertically
async def resize_view(width: int = 128, height: int = 128, file:UploadFile = File(...)):
    bytes_str = io.BytesIO(await file.read())
    try:
        img = Image.open(bytes_str)
    except:
        raise HTTPException(detail="Invalid image", status_code=400)
    size = width, height
    img = resize(img, size)
    fname = pathlib.Path(file.filename)
    fext = fname.suffix # .jpg, .txt
    dest = UPLOAD_DIR / f"{uuid.uuid1()}{fext}"
    img.save(dest)
    return dest 

# counter clock-wise, keeps the same size
def rotate(img: Image, degrees: int) -> Image: 
    if degrees == 90:
        return img.transpose(Image.ROTATE_90)
    elif degrees == 180:
        return img.transpose(Image.ROTATE_180)
    elif degrees == 270:
        return img.transpose(Image.ROTATE_270)
    else: 
        return img.rotate(degrees) # size stays the same for sure

@app.post("/rotate/", response_class=FileResponse) # flip the image horizontally or vertically
async def rotate_view(degrees: int = 90, file:UploadFile = File(...)):
    bytes_str = io.BytesIO(await file.read())
    try:
        img = Image.open(bytes_str)
    except:
        raise HTTPException(detail="Invalid image", status_code=400)

    img = rotate(img, degrees)
    fname = pathlib.Path(file.filename)
    fext = fname.suffix # .jpg, .txt
    dest = UPLOAD_DIR / f"{uuid.uuid1()}{fext}"
    img.save(dest)
    return dest 


        
# async def process_operation(img: Image, custom_param: ImgEditParam) -> Image: 
#     if custom_param.name == "flip": 
#         return flip(img, custom_param.toggle)
#     if custom_param == "greyscale": 
#         return greyscale(img)
#     return img
    
# @app.post("/api/v1/", response_class=FileResponse)
# async def edit_multiple_images(operations: List[ImgEditParam], file:UploadFile = File(...)) -> Image:
#     bytes_str = io.BytesIO(await file.read())
#     try:
#         img = Image.open(bytes_str)
#     except:
#         raise HTTPException(detail="Invalid image", status_code=400)
#     if operation is None: 
#         raise HTTPException(detail="Missing Image Edit Parameters", status_code=400)

#     for operation in operations: 
#         print("--------Processing Operation: " + operation.name)
#         #  img = process_operation(img, operation)
#     return img

@app.post("/api/v1/testing")
async def edit_multiple_images_test(operations: List[ImgEditParam]):
    if operation is None: 
        raise HTTPException(detail="Missing Image Edit Parameters", status_code=400)

    for operation in operations: 
        print("--------Processing Operation: " + operation.name)
        #  img = process_operation(img, operation)