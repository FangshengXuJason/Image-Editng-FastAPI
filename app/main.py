import pathlib
import os
import io
from fastapi import(
    FastAPI
    )

app = FastAPI()

@app.get('/')
def home_view():
    return {"key": "value"}



