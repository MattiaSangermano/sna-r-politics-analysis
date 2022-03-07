import requests

from .user import user

def comment(id, headers, users):
    res = requests.get(
        'https://oauth.reddit.com/api/info/',
        params={
            'id': id
        },
        headers = headers
    )
    status_code = res.status_code
    if(status_code == 200):
        req_results = res.json()['data']['children']
        results = {}
        last_result = {}
        for children in req_results:
            result = children['data']
        
            # Filter the comment attributes
            filtered_result = {
                'id': result['name'],
                'total_awards_received': result['total_awards_received'],
                'score': result['score'],
                'downs': result['downs'],
                'ups': result['ups'],
                'num_reports': result['num_reports'],
                'likes': result['likes'],
                'body': result['body'],
                'parent_id': result['parent_id'],
                'link_id': result['link_id'],
                'created_at': int(result['created_utc'])
            }
            if 'author_fullname' in result:
                if result['author_fullname'] in users:
                    filtered_result['author'] = users[result['author_fullname']]
                else:
                    user_status_code, user_result = user(result['author_fullname'], headers)
                    if user_status_code == 200: 
                        filtered_result['author'] = user_result
                    else:
                        filtered_result['author'] = user_status_code
                    users[result['author_fullname']] = filtered_result['author']
            else:
                filtered_result['author'] = '@Error:404_not_found'
            
            results[filtered_result['id']] = filtered_result
            last_result = filtered_result

        return status_code, results, last_result

    return status_code, None, None