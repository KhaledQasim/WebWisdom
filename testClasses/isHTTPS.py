from urllib.parse import urlparse
from http.client import HTTPConnection, HTTPSConnection

BASE_URL = 'mail.qasimfiles.uk'

def check_https_url(url):
    # HTTPS_URL = f'https://{url}'
    # try:
    #     HTTPS_URL = urlparse(HTTPS_URL)
    #     connection = HTTPSConnection(HTTPS_URL.netloc, timeout=2)
    #     connection.request('HEAD', HTTPS_URL.path)
    #     if connection.getresponse():
    #         return True
    #     else:
    #         return False
    # except:
    return False

def check_http_url(url):
    HTTP_URL = f'http://{url}'
    try:
        HTTP_URL = urlparse(HTTP_URL)
        connection = HTTPConnection(HTTP_URL.netloc)
        connection.request('HEAD', HTTP_URL.path)
        if connection.getresponse():
            return True
        else:
            return False
    except:
        return False


if check_https_url(BASE_URL):
    print("Nice, you can load the website with HTTPS")
elif check_http_url(BASE_URL):
    print("HTTPS didn't load the website, but you can use HTTP")
else:
    print("Both HTTP and HTTPS did not load the website, check whether your url is malformed.")