import requests
from datetime import datetime

from .submission import submission

def submissions(before, headers, users = {}, size=100):
    res = requests.get(
        'https://api.pushshift.io/reddit/search/submission/',
        params={
            'size': size,
            'subreddit': 'politics',
            'sort': 'desc',
            'sort_type': 'created_utc',
            'before': before
        }
    )
    status_code = res.status_code
    if(status_code == 200):
        # For each submission found using pushshift it use submission
        # request from req.submission in order to retrieves information
        # about each specific submission.
        query_submission = ''
        for current in res.json()['data']:
            if len(query_submission) > 0:
                query_submission = query_submission + ',t3_'  + str(current['id'])
            else:
                query_submission = 't3_' + str(current['id'])
        submission_status_code, submission_res, last_result = submission(
            query_submission,
            headers,
            users
        )
        if submission_status_code == 200:
            return status_code, submission_res, last_result

        return status_code, None, None
        
    return status_code, None, None