import json
import time
from os import environ
from typing import Dict

import requests


class SlackClient(object):
    EARNING_ID = 'CQAJU08DR'
    OPTION_BOT_ID = 'CQPRPNC7R'

    def __init__(self) -> None:
        self._token = environ.get('SLACK_TOKEN')
        if self._token is None:
            raise Exception('Missing SLACK_TOKEN')

    def _gen_header(self) -> Dict[str, str]:
        return {
            'Authorization': f'Bearer {self._token}',
            'Content-Type': 'application/json',
        }

    def _post_to_channel(self, msg: str, channel_id: str) -> None:
        session = requests.session()
        session.headers = self._gen_header()
        data = str.encode(json.dumps({
            'channel': channel_id,
            'text': msg,
        }))
        response = session.post('https://slack.com/api/chat.postMessage', data=data)
        if response.status_code != 200:
            time.sleep(5)
            self._post_to_channel(msg=msg, channel_id=channel_id)

    def post_to_option_bot(self, msg: str) -> None:
        self._post_to_channel(msg=msg, channel_id=self.OPTION_BOT_ID)

    def post_to_earning(self, msg: str) -> None:
        self._post_to_channel(msg=msg, channel_id=self.EARNING_ID)


slack_client = SlackClient()
