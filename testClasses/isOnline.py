import requests

def isOnline(target):
    """Check if target domain is online.
    
    Args:
        (string): the domain to be checked
        
    Returns:
        (boolean): True if online, False if offline
    """
   
    url_response = requests.get(target)
    if url_response.status_code == 200:
        return True
    else:
        return False

