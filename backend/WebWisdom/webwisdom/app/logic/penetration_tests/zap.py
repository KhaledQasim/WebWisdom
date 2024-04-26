# tests/example_test.py

from bs4 import BeautifulSoup
from fastapi import HTTPException
from ..base_test import BaseTest
import asyncio
import os 
from datetime import datetime
from pathlib import Path
import aiofiles
from .. import score_calculator

class ZAP(BaseTest):
    def __init__(self,url):
        self.url = url
        
    
    async def get_report(self):
        """Retrieves the report from the penetration tool provided by zap https://www.zaproxy.org/docs/docker/baseline-scan/

        Args:
            url (http_url): url of website to test

        Returns:
            report (str): entire report returned as a string
        """
        print("inside get_report in file zap.py, url is: ",self.url)
        
          
        risk_score_mapping = {
            'High': 4,
            'Medium': 2,
            'Low': 1
        }
        
        
        # offline test support 
        if self.url == "https://test.test/":
            
            report_path = Path(os.getcwd()) / "testreport.html"
            report_content = False  # Default content if file doesn't exist
            
            
            if report_path.exists():
                async with aiofiles.open(report_path,mode="r") as file:
                    report_content = await file.read()
                       
            else:
                print("no report html content generated")   
            
            if report_content is False:
                return "Could not generate html report using zap",0    
            
            soup = BeautifulSoup(report_content, 'html.parser')
        
            # find the first table that matches the class=summary
            summary_table = soup.find('table', class_='summary')
            
            
            results = []
            
            if summary_table:
                rows = summary_table.find_all('tr')
                
                for row in rows:
                    cells = row.find_all('td')
                    if len(cells) == 2:  # Ensure there are exactly two cells
                        risk_level = cells[0].text.strip()
                        number_of_alerts = cells[1].text.strip()
                        
                        # Check for specific risk levels and append to results if matched
                        if risk_level == 'High':
                            results.append({"High": int(number_of_alerts)})
                        elif risk_level == 'Medium':
                            results.append({"Medium": int(number_of_alerts)})
                        elif risk_level == 'Low':
                            results.append({"Low": int(number_of_alerts)})
            
         
            results_for_score_calculator = []
            for result in results:
                for risk_level , count in result.items():
                    if risk_level in risk_score_mapping:
                        score = risk_score_mapping[risk_level]
                        results_for_score_calculator.extend([score]*count)    
            
          
          
            score = score_calculator.calculate_security_score_from_list(results_for_score_calculator)
            print("zap offline done")
            return report_content,score
            
    
        
        
        
        
        
        
        
        
        
        
        
        # actual normal test against online sites
        current_datetime = datetime.now()
        time = current_datetime.strftime('%Y-%m-%d_%H-%M-%S')
        test_report_with_time = f"testreport{time}.html"
        command = f'docker run --network="host" -v $(pwd):/zap/wrk/:rw -t ghcr.io/zaproxy/zaproxy:stable zap-baseline.py -t {self.url} -r {test_report_with_time}'

        process = await asyncio.create_subprocess_shell(
            command, stdout=asyncio.subprocess.PIPE,stderr=asyncio.subprocess.PIPE)
        stdout , stderr = await process.communicate()
        
        print("zap scan results",stdout.decode())
        
        if stderr:
            print("Error in ptt scan:", stderr.decode())
            return "error in generating ZAP report , check logs",2
        
        
      
        
 
        report_path = Path(os.getcwd()) / test_report_with_time
        report_content = False  # Default content if file doesn't exist
        
        
        if report_path.exists():
            async with aiofiles.open(report_path,mode="r") as file:
                report_content = await file.read()
            os.remove(report_path)         
        else:
            print("no report html content generated")   
           
       
        
        
        if report_content is False:
            return "Could not generate html report using zap",0    
        
        
        
        
        
        soup = BeautifulSoup(report_content, 'html.parser')
        
        # find the first table that matches the class=summary
        summary_table = soup.find('table', class_='summary')
        
        
        results = []
        
        if summary_table:
            rows = summary_table.find_all('tr')
            
            for row in rows:
                cells = row.find_all('td')
                if len(cells) == 2:  # Ensure there are exactly two cells
                    risk_level = cells[0].text.strip()
                    number_of_alerts = cells[1].text.strip()
                    
                    # Check for specific risk levels and append to results if matched
                    if risk_level == 'High':
                        results.append({"High": int(number_of_alerts)})
                    elif risk_level == 'Medium':
                        results.append({"Medium": int(number_of_alerts)})
                    elif risk_level == 'Low':
                        results.append({"Low": int(number_of_alerts)})
        
        
      
        results_for_score_calculator = []
        for result in results:
            for risk_level , count in result.items():
                if risk_level in risk_score_mapping:
                    score = risk_score_mapping[risk_level]
                    results_for_score_calculator.extend([score]*count)    
        
        
          
        score = score_calculator.calculate_security_score_from_list(results_for_score_calculator)
      
        print("zap done")
        
        
        
        return report_content,score
        
  
        
       
    
    async def run_test(self):
        # Simulate a test
        report,score = await self.get_report()
        return report,score
  