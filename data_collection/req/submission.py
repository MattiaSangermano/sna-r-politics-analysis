import requests
import time

from .comments import comments
from .user import user

def submission(id, headers, users):
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
            # Filter the submission attributes and create the corresponding dataframe
            filtered_result = {
                'id': result['name'],
                'title': result['title'],
                'upvote_ratio': result['upvote_ratio'],
                'ups': result['ups'],
                'downs': result['downs'],
                'is_original_content': result['is_original_content'],
                'score': result['score'],
                'num_comments': result['num_comments'],
                'num_crossposts': result['num_crossposts'],
                'created_at': int(result['created_utc']),
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

            # Retrieves all the comments belonging to the submission
            comments_res = {}
            comments_status_code, comments_temp, last_result = comments(filtered_result['id'], int(time.time()), headers, users)
            while(comments_status_code == 200 and comments_temp != None and len(comments_temp) > 0):
                comments_res.update(comments_temp)
                comments_status_code, comments_temp, last_result = comments(filtered_result['id'], last_result['created_at'] + 1.0, headers, users)
            filtered_result['comments'] = comments_res

            results[filtered_result['id']] = filtered_result
            last_result = filtered_result
                
        return status_code, results, last_result

    return status_code, None, None