import requests
from datetime import datetime

from .comment import comment

def comments(link_id, before, headers, users, size=100):
    res = requests.get(
        'https://api.pushshift.io/reddit/comment/search/',
        params={
            'link_id': link_id,
            'limit': size,
            'sort': 'desc',
            'sort_type': 'created_utc',
            'before': before
        }
    )
    status_code = res.status_code
    if(status_code == 200):
        # For each comments found using pushshift it use comments
        # request from req.comments in order to retrieves information
        # about each specific comments.
        query_comment = ''
        for current in res.json()['data']:
            if len(query_comment) > 0:
                query_comment = query_comment + ',t1_'  + str(current['id'])
            else:
                query_comment = 't1_' + str(current['id'])
                
        comment_status_code, comment_res, last_result = comment(
            query_comment,
            headers,
            users
        )
        if comment_status_code == 200:
            return status_code, comment_res, last_result
        return status_code, None, None
    return status_code, None, None