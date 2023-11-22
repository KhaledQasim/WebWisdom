from urllib.parse import urlparse
from http.client import HTTPConnection, HTTPSConnection
import requests


# def check_https_url(url):
#     HTTPS_URL = f'https://{url}'
#     try:
#         HTTPS_URL = urlparse(HTTPS_URL)
#         connection = HTTPSConnection(HTTPS_URL.netloc, timeout=2)
#         connection.request('HEAD', HTTPS_URL.path)
#         if connection.getresponse():
#             return True
#         else:
#             return False
#     except:
#         return False


def isHttps(domain):
    try:
        url_response_https = requests.get(f"https://{domain}", timeout=2.5)
        if (url_response_https.status_code == 200):
            return True
    except:
        return False


# def check_http_url(url):
#     HTTP_URL = f'http://{url}'
#     try:
#         HTTP_URL = urlparse(HTTP_URL)
#         connection = HTTPConnection(HTTP_URL.netloc)
#         connection.request('HEAD', HTTP_URL.path)
#         if connection.getresponse():
#             return True
#         else:
#             return False
#     except:
#         return False

def isHttp(domain):
    try:
        url_response_http = requests.get(f"http://{domain}", timeout=2.5)
        if (url_response_http.status_code == 200):
            return True
        else:
            return False
    except:
        return False


def CheckOnlineAndHttp(url):
    if isHttps(url):
        return "Server is Online and Using HTTPS"
    elif isHttp(url):
        return "Server is Online but can not use HTTPS , only HTTP"
    else:
        return "Domain is down or the inputted domain is malformed!"


