slack_token = 'xoxb-my-bot-token'
slack_channel = '#my-channel'
slack_icon_url = 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTuGqps7ZafuzUsViFGIremEL2a3NR0KO0s0RTCMXmzmREJd5m4MA&s'
slack_user_name = 'Double Images Monitor'

import requests
import json

def post_message_to_slack(text, blocks = None):
    return requests.post('https://slack.com/api/chat.postMessage',
    'token': slack_token,
    'channel': slack_channel,
    'text': text,
    'icon_url': slack_icon_url,
    'username': slack_user_name
    'blocks': json.dumps(blocks) if blocks else None
    }).json()


slack_info = 'hello'

post_message_to_slack(slack_info)		