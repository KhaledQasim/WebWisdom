# WebWisdom
A full-stack Fast-API and React tool for automated penetration testing of publicly available websites.
Disclaimer: Only use this tool on websites and domains that you own

# Installation and Deployment
## Requirements
Linux Operating System

Poetry

NPM

Node

Python 3.10.x

Docker 

```bash
docker pull ghcr.io/zaproxy/zaproxy:stable
```

Nmap

```bash
pip install ptt
```


## Steps
Clone the repository:
```bash
git clone https://github.com/KhaledQasim/WebWisdom.git
```
### Fast-API Backend
```bash
cd WebWisdom/backend/WebWisdom
```
Get Fast-API dependencies 
```
poetry install
```
Navigate inside the poetry virtual environment
```
poetry shell
```
```
cd webwisdom
```
Create a .env file in this directory and populate it with the following content
```text
SECRET_KEY="run below command"
ALGORITHM="HS256"
ACCESS_TOKEN_EXPIRE_MINUTES=2880
ALLOWED_FRONTEND_URL="http://127.0.0.1:5174"
```
To Generate a secret key run the below command then copy the output with no spaces and place it a string value for the .env variable "SECRET_KEY"
```bash
openssl rand -base64 64
```
Then start the Fast-API uvicron server
```
poetry run uvicorn webwisdom.main:app --port 8000 --reload
```
If port 8000 is already being used then you must kill the program using it so univron can use it instead


### React Frontend
Navigate into this directory `WebWisdom/frontend`
Run this command to install the frontend react dependencies 
```bash
npm install
```
Then create a .env file and populate it with the following information
```
VITE_BACKEND_URL="http://127.0.0.1:8000"
```
Then build the frontend
```
npm run build
```
Then preview the build and it all should work now
```
npm run preview
```


# Testing
Install Pytest
Navigate to `/WebWisdom/backend/WebWisdom` directory
Open a terminal in the directory and run the command `pytest -v -s`



