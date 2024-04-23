import subprocess
import re


class nmap:
    def __init__(self, url):
        self.url = str(url)

    def nmap_scan(self):
        parsed_url = self.url
        parsed_url = parsed_url.replace("http://", "")
        parsed_url = parsed_url.replace("https://", "")
        parsed_url = parsed_url.rstrip('/')

        command = f'nmap {parsed_url}'
        command_result = subprocess.run(
            command, capture_output=True, text=True, shell=True)

        pattern = r"(\d+)/(\S+)\s+open\s+(\S+)"
        matches = re.finditer(pattern, command_result.stdout)

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
        data = []
        results = []
        for match in matches:
            port, protocol, service = match.groups()
            result = {
                "port": int(port),
                "protocol": protocol,
                "service": service
            }
            data.append(result)


        results.append({"data":data})
        
        if not data:
            print("nmap scan could not return open ports.")

        for x in data:
            if ('port' in x and 'service' in x):
                if (x["port"] == 3306 and x["service"].lower() == "mysql".lower()):
                    print("MySQL found")
                    results.append({"VulnerabilityFound": {
                        "detail": "MySQL database service should not be publicly exposed since it likely stores sensitive information about the site!",
                        "RiskLevel": "Risk Level: 2"
                    }})
                    results.append({"total_risk_mysql":[2]})

        

        return results
