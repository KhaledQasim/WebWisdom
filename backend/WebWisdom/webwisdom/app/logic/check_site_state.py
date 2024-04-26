import dns.resolver
import socket
import ssl



class check_site_state:
    """Checks if a site's domain exists by searching for A records, then checks for proper use of https , returns a dictionary of the findings
    """
    def __init__(self, site):
        self.site = str(site)
    
    async def check_site_is_online(self):
        """Checks if a site has A records and if it is online via socket connections on ports 80 and 443, also checks that the ssl connection is working correctly 

        Args:
            site (string): complete site url to test, e.g: https://example.com

        Returns:
            Boolean: True if online False if not
        """
        try:
            results={
                "port_80":False,
                "port_443":False,
                "message":"",
                "url":str(self.site),
                "ssl":False
            }
              
            # Getting the A records for the site
            answers = dns.resolver.resolve(self.site, 'A')
            print(f"A records for {self.site}:")
            IP_number=0
            for rdata in answers:
              
                IP_number+=1
                print('IP:', rdata.address)
                results[f'IP_{IP_number}'] = rdata.address
             
 
            
            def check_port(ip, port, timeout=10):
                try:
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    sock.settimeout(timeout)
                    if port == 443:  # If port 443, wrap the socket with SSL
                        context = ssl.create_default_context()
                        sock = context.wrap_socket(sock, server_hostname=self.site)
                    result = sock.connect_ex((ip, port))
                    sock.close()
                    return result == 0
                except Exception as e:
                    print(f"Error connecting to {ip} on port {port}: {e}")
                    return False

            # Checking each port with the retrieved A records
            online = False
            for rdata in answers:
                ip = rdata.address
            
                if check_port(ip, 80):
                    print(f"{self.site} (IP: {ip}) is online on port 80!")
                    online = True
                    results["port_80"] = True
                    
                if check_port(ip, 443):
                    print(f"{self.site} (IP: {ip}) is online on port 443 with SSL!")
                    online = True
                    results["port_443"] = True
                    results["ssl"]= True
                    
                  


            if not online:
                print(f"{self.site} is not responding on ports 80 or 443.")
                results["message"]=f"{self.site} is not responding on ports 80 or 443."
                # return False, f"{self.site} is not responding on ports 80 or 443."

        
        except dns.resolver.NoAnswer:
            print(f"No A records found for {self.site}")
            results["message"]=f"No A records found for {self.site}"
            # return False, f"No A records found for {self.site}"
        except dns.resolver.NXDOMAIN:
            print(f"Site {self.site} does not exist")
            results["message"]=f"No A records found for {self.site}"
            # return False, f"Site {self.site} does not exist"

        except Exception as e:
            print(f"An error occurred in check_site_is_online: {e}")
            results["message"]=f"An error occurred in checking if site is online please confirm that the site url is working"
            # return False, f"An error occurred in checking if site is online please confirm that the site url is working"

        return results

