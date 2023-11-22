from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import webwisdom_poetry.isHTTPS as isHTTPS

app = FastAPI()

origins = [
    "http://localhost:3000",
    "localhost:3000"
]

todos = [
    {
        "id": "1",
        "item": "Read a book."
    },
    {
        "id": "2",
        "item": "Cycle around town."
    }
]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


@app.get("/", tags=["root"])
async def read_root() -> dict:
    return {"message": "Welcome to your todo list."}


@app.get("/todo", tags=["todos"])
async def get_todos() -> dict:
    return {"data": todos}


# @app.get("/online", tags=["online"])
# async def get_online() -> dict:
#     return {"data": isHTTPS.isOnline("mail.qasimfiles.uk")}


@app.post("/online")
def getOnline(domain: dict):
  
    return {"data": isHTTPS.CheckOnlineAndHttp(domain["data"])}
