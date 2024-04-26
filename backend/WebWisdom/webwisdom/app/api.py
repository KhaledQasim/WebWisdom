from fastapi import Depends, APIRouter, HTTPException, status, Cookie, FastAPI, Response
from aiohttp import ClientSession
# from .logic.framework import WordPress
from .logic import check_site_state
from bs4 import BeautifulSoup
import requests
from ..database import schemas
from .logic import data_parse
from .logic import score_calculator
from typing import Annotated, List
from ..routers import auth
from sqlalchemy.orm import Session
import json
from ..database.schemas import SecurityData
import os
import importlib
from .logic.base_test import BaseTest
from pathlib import Path

router = APIRouter(
    prefix="/api",
    tags=["api"],
    # dependencies=[Depends(oauth2_scheme)],
)


def calc(data1: list[int], data2: list[int]):
    all_data = []
    if isinstance(data1, list) and isinstance(data2, list):
        all_data += data1
        all_data += data2
        print(all_data)
    else:
        print("data not list")


@router.get("/temp/testing")
async def testing():
    current_directory = os.getcwd()
    report_path = current_directory+("/testreport.html")
    print(report_path)
    
    path = Path(report_path)
    new_name = current_directory+"/testreport2.html"
    
    if path.exists():
        with path.open('r') as file:
            report_content = file.read()
            
            print("report content as string : ",str(report_content))
            os.rename(report_path,new_name)
    else:
        print("no report html content generated")   
        
    return {"data":1}


@router.get("/test-parse")
async def Test_parse(user: Annotated[schemas.User, Depends(auth.get_current_active_user)], db: Session = Depends(auth.get_db)):
    try:
        user_info = await auth.get_current_active_user(user)

    except Exception as e:
        print("Error in Start_scan first try block", e)
        raise HTTPException(status_code=401, detail="Unauthorized")

    ssl = False
    data = data_parse.formate_report_test(ssl)
    result = {

        "connection_and_records": {
            "port_80": True,
            "port_443": False,
            "message": "",
            "url": "testurl.com",
            "ssl": False,
            "IP_1": "35.44.22.33"
        },
        "data": data
    }

    auth.crud.create_user_test_result(
        db=db, result=json.dumps(result), user_id=1)

    saved_result = auth.crud.get_latest_user_result(db=db, user_id=1)

    print(saved_result.id)

    return {
        "id": int(saved_result.id),
        "connection_and_records": {
            "port_80": True,
            "port_443": False,
            "message": "",
            "url": "testurl.com",
            "ssl": False,
            "IP_1": "35.44.22.33"
        },
        "data": data
    }


@router.post("/start-scan")
async def Start_scan(User_provided_url: schemas.URL, user: Annotated[schemas.User, Depends(auth.get_current_active_user)], db: Session = Depends(auth.get_db)):
    try:
        user_info = await auth.get_current_active_user(user)

    except Exception as e:
        print("Error in Start_scan first try block", e)
        raise HTTPException(status_code=401, detail="Unauthorized")

    try:
        run_helper = check_site_state.check_site_state(
            str(User_provided_url.url.host))
        result_check_site = run_helper.check_site_is_online()

        print("main")
        print(result_check_site["port_80"], result_check_site["port_443"])

        if (result_check_site["port_80"] == False and result_check_site["port_443"] == False):
            raise HTTPException(
                status_code=405, detail="Site is down or does not exist please check the url and that the site is accessible and running!")

        ssl = True
        if (result_check_site["ssl"] == False):
            ssl = False

        data = data_parse.formate_report(User_provided_url.url, ssl)

        result = {
            "connection_and_records": result_check_site,
            "data": data
        }

        auth.crud.create_user_test_result(
            db=db, result=json.dumps(result), user_id=user_info.id)

        saved_result = auth.crud.get_latest_user_result(
            db=db, user_id=user_info.id)

        return {
            "id": int(saved_result.id),
            "connection_and_records": result_check_site,
            "data": data
        }

    except ValueError as e:
        print("Error", e)
        return {"error": "Invalid operation"}

    # for evidence in evidences:
    #     print(evidence


@router.post("/calculate-security-score-test/")
async def calculate_security_score(data: SecurityData):

    return score_calculator.calculate_security_score_from_list(data.data)


@router.get("/get-vulnerability-score-test")
async def get_vulnerability_score_test():
    return score_calculator.get_vulnerability_scores_from_report_and_calculate()


def load_tests(ssl, url):
    """load the python test modules dynamically 

    Returns:
        tests: returns the loaded tests
    """
    tests = {}
    directory = 'webwisdom/app/logic/penetration_tests'
    for filename in os.listdir(directory):
        if filename.endswith(".py") and not filename.startswith("__"):
            module_name = filename[:-3]
            module = importlib.import_module(
                f"webwisdom.app.logic.penetration_tests.{module_name}")
            for item in dir(module):
                obj = getattr(module, item)
                if isinstance(obj, type) and issubclass(obj, BaseTest) and obj is not BaseTest:
                    # Pass ssl variable to PTT test, all other tests do not receive variables
                    if item == "PTT":
                        instance = obj(ssl, url)
                        tests[item] = instance
                    else:
                        instance = obj(url)
                        tests[item] = instance

    return tests


@router.post("/run-tests")
async def run_tests(User_provided_url: schemas.URL, user: Annotated[schemas.User, Depends(auth.get_current_active_user)], db: Session = Depends(auth.get_db)):
    """endpoint to start the penetration tests , use the url https://test.test/ for test data to be returned

    Args:
        User_provided_url (schemas.URL): url from user
        user (Annotated[schemas.User, Depends): user authentication
        db (Session, optional): _description_. Defaults to Depends(auth.get_db).

    Raises:
        HTTPException: _description_
        HTTPException: _description_

    Returns:
        _type_: _description_
    """
    results = []
    url = str(User_provided_url.url)
    try:
        user_info = await auth.get_current_active_user(user)

    except Exception as e:
        print("Error in Start_scan first try block", e)
        raise HTTPException(status_code=401, detail="Unauthorized")

    try:
        print("user provided url in run_tests method in api.py: ",
              User_provided_url.url)
        if str(User_provided_url.url) == "https://test.test/":
            ssl = 4
            tests = load_tests(ssl=4, url=url)
            result_check_site = {

                "port_80": True,
                "port_443": False,
                "message": "",
                "url": "testurl.com",
                "ssl": False,
                "IP_1": "35.44.22.33"
            }
            results.append({"test": "connection_and_records",
                           "report": result_check_site, "score": ssl})

            for test_name, test_instance in tests.items():
                report, score = await test_instance.run_test()
                results.append(
                    {"test": test_name, "report": report, "score": score})

            auth.crud.create_user_test_result(
                db=db, result=json.dumps(results), user_id=user_info.id)

            saved_result = auth.crud.get_latest_user_result(
                db=db, user_id=user_info.id)

            results.append({"id": int(saved_result.id)})
            return {"data": results}

        else:
            run_helper = check_site_state.check_site_state(
                str(User_provided_url.url.host))
            result_check_site = await run_helper.check_site_is_online()

            print(result_check_site["port_80"], result_check_site["port_443"])

            if (result_check_site["port_80"] == False and result_check_site["port_443"] == False):
                raise HTTPException(
                    status_code=405, detail="Site is down or does not exist please check the url and that the site is accessible and running!")

            ssl = 0
            if (result_check_site["ssl"] == False):
                ssl = 4

            tests = load_tests(ssl=ssl, url=url)

            results.append({"test": "connection_and_records",
                           "report": result_check_site, "score": ssl})
            for test_name, test_instance in tests.items():
                report, score = await test_instance.run_test()
                results.append(
                    {"test": test_name, "report": report, "score": score})

            auth.crud.create_user_test_result(
                db=db, result=json.dumps(results), user_id=user_info.id)

            saved_result = auth.crud.get_latest_user_result(
                db=db, user_id=user_info.id)

            results.append({"id": int(saved_result.id)})
            return {"data": results}

    except ValueError as e:
        print("Error", e)
        return {"error": "Invalid operation"}
