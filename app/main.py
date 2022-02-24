from curses import noecho
import pathlib
import os
import io
from typing import Optional, Tuple
from urllib import response
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
from pydantic import BaseSettings
from PIL import Image
from typing import List, Tuple

# system config
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

# path config
BASE_DIR = pathlib.Path(__file__).parent
UPLOAD_DIR = BASE_DIR / "uploads" # for indiviual operation testing
TEMP_DIR = BASE_DIR / "temps" # for API testing


app = FastAPI()
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))


# welcome page for live demo
@app.get("/", response_class=HTMLResponse) # http GET -> JSON
def home_view(request: Request):
    return templates.TemplateResponse("home.html", {"request": request, "author": "Fangsheng Xu"})


def flip(img: Image, top_bottem: bool) -> Image: 
    if top_bottem: 
        return img.transpose(Image.FLIP_TOP_BOTTOM)
    else: 
        return img.transpose(Image.FLIP_LEFT_RIGHT)


def greyscale(img: Image) -> Image: 
    return  img.convert('L')


def resize(img: Image, size: Tuple[int, int]) -> Image: 
    return img.resize(size)

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


@app.post("/api/v1/upload/") # flip the image horizontally or vertically
async def upload_image(file:UploadFile = File(...)):
    bytes_str = io.BytesIO(await file.read())
    try:
        img = Image.open(bytes_str)
    except:
        raise HTTPException(detail="Invalid image", status_code=400)

    fname = pathlib.Path(file.filename)
    fext = fname.suffix # .jpg, .txt
    dest = TEMP_DIR / f"{uuid.uuid1()}{fext}"
    img.save(dest)
    return dest


@app.get("/api/v1/downlaod/{file_path: path}", response_class=FileResponse)
async def download_image(file_path: str):
    # verify file_path
    file_name = pathlib.Path(file_path)
    if not file_name.exists(): 
        raise HTTPException(detail="Invalid path", status_code=400)
    return file_path


@app.put("/api/v1/flip/{file_path: path}") 
async def flip_api(file_path: str, top_bottem: bool = True):
    try:
        img = Image.open(file_path)
    except:
        raise HTTPException(detail="Invalid path", status_code=400)
    img = flip(img, top_bottem)
    img.save(file_path)
    if top_bottem: 
        return {"operation": "flip top and bottem"}
    return {"operation": "flipped left and right"}


@app.put("/api/v1/greyscale/{file_path: path}") 
async def greyscale_api(file_path: str):
    try:
        img = Image.open(file_path)
    except:
        raise HTTPException(detail="Invalid path", status_code=400)
    img = greyscale(img)
    img.save(file_path)
    return {"operation": "greyscale"}


@app.put("/api/v1/resize/{file_path: path}")
async def resize_api(file_path: str, width: int = 128, height: int = 128):
    try:
        img = Image.open(file_path)
    except:
        raise HTTPException(detail="Invalid path", status_code=400)
    size = width, height
    img = resize(img, size)
    img.save(file_path)
    return {"operation": "resized to " + str(width) + " x " + str(height)}


@app.put("/api/v1/rotate/{file_path: path}")
async def rotate_api(file_path: str, degrees: int = 90):
    try:
        img = Image.open(file_path)
    except:
        raise HTTPException(detail="Invalid path", status_code=400)
    img = rotate(img, degrees)
    img.save(file_path)
    return {"operation": "rotated enouter close-wise by" + str(degrees) + "degrees"}