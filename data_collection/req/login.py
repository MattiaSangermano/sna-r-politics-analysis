import requests

def login(clientId, secretToken, username, password, userAgent):
    res = requests.post(
        'https://www.reddit.com/api/v1/access_token',
        auth = requests.auth.HTTPBasicAuth(
            clientId, 
            secretToken
        ), 
        data = {
            'grant_type': 'password',
            'username': username,
            'password': password
        },
        headers = {
            'User-Agent': userAgent
        }
    )
    if res.status_code == 401:
        return 0
    return {
        'User-Agent': userAgent, 
        'Authorization': f'bearer {res.json()["access_token"]}'
    }
