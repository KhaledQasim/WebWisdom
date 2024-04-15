from fastapi import Depends, APIRouter, HTTPException, status, Cookie, FastAPI, Response
from aiohttp import ClientSession
# from .logic.framework import WordPress
from fastapi import status as http_status
from .logic import check_site_state
from bs4 import BeautifulSoup
import requests
from ..database import schemas
from .logic import data_parse
from typing import Annotated
from ..routers import auth
from sqlalchemy.orm import Session
import json

router = APIRouter(
    prefix="/api",
    tags=["api"],
    # dependencies=[Depends(oauth2_scheme)],
)



@router.post("/test-parse")
async def Test_parse(db: Session = Depends(auth.get_db)):

     
    data = data_parse.formate_report_test()
    result = { "connection_and_records": "result_check_site",
        "data": data}

   
   
    auth.crud.create_user_test_result(db=db, result=json.dumps(result), user_id=1)
    return {
        "connection_and_records": "result_check_site",
        "data": data
    }
 


@router.post("/start-scan")
async def Start_scan(User_provided_url: schemas.URL, user: Annotated[schemas.User, Depends(auth.get_current_active_user)],db: Session = Depends(auth.get_db)):
    try:
        user_info = await auth.get_current_active_user(user)
        
    except Exception as e:
        print("Error in Start_scan first try block",e)
        raise HTTPException(status_code=401,detail="Unauthorized")
    
    
    try:
        run_helper = check_site_state.check_site_state(str(User_provided_url.url.host))
        result_check_site = run_helper.check_site_is_online()
        
        print("main")
        print(result_check_site["port_80"],result_check_site["port_443"])
        
        if(result_check_site["port_80"]==False and result_check_site["port_443"] == False):
            return {"error":"Site is down or does not exist please check the url and that the site is accessible and running!"}
        data = data_parse.formate_report(User_provided_url.url)

        result = {
            "connection_and_records": result_check_site,
            "data": data    
        }

        auth.crud.create_user_test_result(db=db, result=json.dumps(result), user_id=user_info.id)
        
        return {
            "connection_and_records": result_check_site,
            "data": data
        }
    
       
    except ValueError as e:
        print("Error", e)
        return {"error": "Invalid operation"}



    
    # for evidence in evidences:
    #     print(evidence
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
