import shutil
import time
import io
from fastapi.testclient import TestClient
from app.main import app, BASE_DIR, UPLOAD_DIR, get_settings

from PIL import Image, ImageChops

client = TestClient(app)

def test_get_home():
    response = client.get("/") # requests.get("") # python requests
    assert response.text != "<h1>Hello world</h1>"
    assert response.status_code == 200
    assert  "text/html" in response.headers['content-type']

# def test_prediction_upload():
#     img_saved_path = BASE_DIR / "images"
#     settings = get_settings()
#     for path in img_saved_path.glob("*"):
#         try:
#             img = Image.open(path)
#         except:
#             img = None
#         response = client.post("/",
#             files={"file": open(path, 'rb')},
#             headers={"Authorization": f"JWT {settings.app_auth_token}"}
#         )
#         if img is None:
#             assert response.status_code == 400
#         else:
#             # Returning a valid image
#             assert response.status_code == 200
#             data = response.json()
#             assert len(data.keys()) == 2
