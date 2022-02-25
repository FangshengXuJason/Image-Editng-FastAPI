# ms-fastapi-django
Hi, I have to tested this on a different machine or on the cloud, but the following instruction should be enough

In order to run on your local machine: 
1. set up python env, make sure that you have all modules in requirements.txt downlaoded; this program is built on python 3.8.12
# install some dependency(helpful commmand)
pip install -r requirements.txt

2. create folder "temps" and "uploads" under /apps/(if they are not there)

3. use uvicorn to run local server(you have to install this module as well)
# RUN LOCAL SERVER Environment
uvicorn app.main:app --reload
