import requests


def isHttps(domain):
    try:
        url_response_https = requests.get(f"https://{domain}", timeout=2.5)
        if (url_response_https.status_code == 200):
            return True
    except:
        return False
        
    
    
def isHttp(domain):
    try:
        url_response_http = requests.get(f"http://{domain}", timeout=2.5)
        if (url_response_http.status_code == 200):
            return True
        else:
            return False
    except:
        return False
    
def CheckOnlineAndHttp(domain):
    if isHttps(domain):
        print("Server is Online and Using HTTPS")    
    elif isHttp(domain):
        print("Server is Online but can not use HTTPS but can use HTTP")
    else:
        print("Domain is down or the inputted domain is malformed!")
# def isHTTPS(domain):
