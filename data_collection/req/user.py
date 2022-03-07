import requests

def user(id, headers):
    res = requests.get(
        'https://oauth.reddit.com/api/user_data_by_account_ids/',
        params={
            'ids': id
        },
        headers = headers
    )
    status_code = res.status_code
    if(status_code == 200):
        result = res.json()[id]
        
        # Filter the user attributes
        return status_code, {
            'id': id,
            'name': result['name'],
            'link_karma': result['link_karma'],
            'comment_karma': result['link_karma'],
            'created_at': int(result['created_utc'])
        }
    
    return status_code, None