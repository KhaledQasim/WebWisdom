from fastapi import Depends, APIRouter, HTTPException, status, Cookie, FastAPI, Response
from .logic.main import hello
from aiohttp import ClientSession
# from .logic.framework import WordPress
from fastapi import status as http_status
from .logic import framework_check
from bs4 import BeautifulSoup
import requests

router = APIRouter(
    prefix="/api",
    tags=["api"],
    # dependencies=[Depends(oauth2_scheme)],
)

   

@router.get("/main")
def Test():
    return {"data":framework_check.JavaScriptFrameworkCheck("http://127.0.0.1:5174/")}
 
