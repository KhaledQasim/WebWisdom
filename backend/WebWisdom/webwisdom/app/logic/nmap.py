import subprocess
import re
import asyncio

from fastapi import HTTPException

class nmap:
    def __init__(self, url):
        self.url = str(url)

    async def nmap_scan(self):
        parsed_url = self.url
        parsed_url = parsed_url.replace("http://", "")
        parsed_url = parsed_url.replace("https://", "")
        parsed_url = parsed_url.rstrip('/')

        command = f'nmap {parsed_url}'
   

        process = await asyncio.create_subprocess_shell(
            command, stdout=asyncio.subprocess.PIPE,stderr=asyncio.subprocess.PIPE)
        stdout , stderr = await process.communicate()
        print(stdout.decode())
        if stderr:
            print("Error in ptt scan:", stderr.decode())
            raise HTTPException(status_code=400, detail="nmap scan failed")
        
        

        pattern = r"(\d+)/(\S+)\s+open\s+(\S+)"
        matches = re.finditer(pattern, stdout.decode())

        results = []
        for match in matches:
            port, protocol, service = match.groups()
            result = {
                "port": int(port),
                "protocol": protocol,
                "service": service
            }
            results.append(result)

        if not results:
            print("no nmap ports scans found")
            results = None
        else:
            for x in results:
                if ('port' in x and 'service' in x):
                    if (x["port"] == 3306 and x["service"].lower() == "mysql".lower()):
                        print("MySQL found")
                        results.append({"VulnerabilityFound": {
                            "detail": "MySQL database service should not be publicly exposed since it likely stores sensitive information about the site!",
                            "RiskLevel": "2"
                        }})
                        results.append({"total_risk_mysql":[4]})

        print(results)
        return results

    def nmap_scan_test(self):
        # command = f'nmap {self.url}'
        # command_result = subprocess.run(command, capture_output=True, text=True, shell=True)
        sample_output = """
        Host is up (0.011s latency).
        Other addresses for yousefqasim.uk (not scanned): 104.21.76.206 2606:4700:3037::6815:4cce 2606:4700:3037::ac43:c90b
        Not shown: 996 filtered ports
        PORT     STATE SERVICE
        80/tcp   open  http
        443/tcp  open  https
        8080/tcp open  http-proxy
        8443/tcp open  https-alt
        3306/tcp open  mysql
        
        Nmap done: 1 IP address (1 host up) scanned in 4.96 seconds
        """

        pattern = r"(\d+)/(\S+)\s+open\s+(\S+)"
        matches = re.finditer(pattern, sample_output)
       
        results = []
        for match in matches:
            port, protocol, service = match.groups()
            result = {
                "port": int(port),
                "protocol": protocol,
                "service": service
            }
            results.append(result)


      
        
        if not results:
            print("nmap scan could not return open ports.")
            results = None
        else:   
            for x in results:
                if ('port' in x and 'service' in x):
                    if (x["port"] == 3306 and x["service"].lower() == "mysql".lower()):
                        print("MySQL found")
                        results.append({"VulnerabilityFound": {
                            "detail": "MySQL database service should not be publicly exposed since it likely stores sensitive information about the site!",
                            "RiskLevel": "Risk Level: 2"
                        }})
                        results.append({"total_risk_mysql":[4]})

        
        print(results)
        return results
