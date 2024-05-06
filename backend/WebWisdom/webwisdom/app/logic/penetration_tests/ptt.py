
# uses a penetration tool provided by https://pentest-tools.com/
from fastapi import HTTPException
from ..base_test import BaseTest
import subprocess
from .. import data_parse,score_calculator
import asyncio


class PTT(BaseTest):
    """Penetration tool provided by https://pentest-tools.com/


    """
    def __init__(self,ssl,url):
        self.ssl = ssl
        self.url = url
        
    async def run_test(self):
        # Simulate a test
        report,score = await self.formate_report()
        return report,score
    
    
    
    
    async def get_vulnerability_report(self):
        """Retrieves the report from the penetration tool provided by https://pentest-tools.com/

        Args:
            url (http_url): url of website to test

        Returns:
            report (str): entire report returned as a string
        """
        print("inside get_vulnerability_report url is",self.url)
        command = f'ptt -q --nocolor run website_scanner {self.url}'

        process = await asyncio.create_subprocess_shell(
            command, stdout=asyncio.subprocess.PIPE,stderr=asyncio.subprocess.PIPE)
        stdout , stderr = await process.communicate()
        
        print(stdout.decode())
        if stderr:
            print("Error in ptt scan:", stderr.decode())
            return "Error in generating base scan!"
        
        
        return stdout.decode()
        
    
    # def test(self):
    #     print(self.url)
    #     print(self.ssl)
    #     return "report from test",2000
  
    async def formate_report(self):
        
        
        dict_list_of_penetration_tests_reports_and_scores = []
        # post data was {
        #                 "url": "https://google.com/"
        #                 }
        # data printed in console was: urlhere from ptt tool:  https://google.com/
        print("urlhere from ptt tool: ", self.url)
        
        if self.url == "https://test.test/":
            reportTest,scoreTest = data_parse.formate_report_test(self.ssl)
            
            return reportTest,scoreTest
        else:    
            report_text =  await self.get_vulnerability_report()
            if "Error in generating base scan!" == report_text:
                return "Error in generating base scan!",0
            
            technologies = data_parse.parse_vulnerability_report_for_technologies(report_text)
            headers = data_parse.parse_vulnerability_report_for_headers(report_text)
            files = data_parse.parse_vulnerability_report_for_txt_files(report_text)
            cookies = data_parse.parse_vulnerability_report_for_insecure_cookie(report_text)
            nmap_object = data_parse.nmap.nmap(str(self.url))
            nmap_scan_result = await nmap_object.nmap_scan()
            server_side_vulnerabilities = data_parse.parse_server_side_vulnerabilities(
                report_text)
            report = [{"technologies": technologies}, {"headers": headers}, {"files": files}, {"cookies": cookies}, {
                "nmap": nmap_scan_result}, {"serverVulnerabilities": server_side_vulnerabilities}]

            data = score_calculator.get_vulnerability_scores_from_report_and_calculate(
                report, self.ssl)
            
            
            
            return report,data

  
  
  
  
  
        
      


