from fastapi import Depends, APIRouter, HTTPException, status, Cookie, FastAPI, Response
from .logic.main import hello
from aiohttp import ClientSession
# from .logic.framework import WordPress
from fastapi import status as http_status
from .logic import framework_check
from bs4 import BeautifulSoup
import requests
from ..database import schemas
from .logic import data_parse



router = APIRouter(
    prefix="/api",
    tags=["api"],
    # dependencies=[Depends(oauth2_scheme)],
)



@router.post("/start-scan")
def Start_scan(User_provided_url: schemas.URL):
    try:
        data = data_parse.formate_report(User_provided_url.url)
        
        # return {"data":get_vulnerability_report(Valid_URL)}
        return data
    except ValueError as e:
        print("Error", e)
        return {"error": "Invalid operation"}



    
    # for evidence in evidences:
    #     print(evidence)