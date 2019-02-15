import json

import requests

from .base_client import WQBaseClient
from .myalphas import WQMyAlphas
from .job import WQJobClient
from .submission import WQSubmissionClient



class WQClient(WQBaseClient):
    def __init__(self):
        super().__init__()

        self.job = WQJobClient(self)
        self.myalphas = WQMyAlphas(self)
        self.submission = WQSubmissionClient(self)

    def get_alphainfo(self, alpha_id):
        r = self.do_post('https://www.worldquantvrc.com/alphainfo', data={
            "args": json.dumps({
                "alpha_list": [alpha_id],
            })
        })

        result = r.json()
        return result['result']['alphaInfo']

    def simulate(self, code, region, universe, decay=20):
        args = [{
            "delay": "1",
            "unitcheck": "off",
            "univid": universe,
            "opcodetype": "FLOWSEXPR",
            "opassetclass": "EQUITY",
            "optrunc": 0.1,
            "code": code,
            "region": region,
            "opneut": "none",
            "IntradayType": None,
            "tags": "equity",
            "decay": decay,
            "dataviz": "0",
            "backdays": 512,
            "simtime": "Y10"
        }]

        r = self.do_post('https://www.worldquantvrc.com/simulate', data={
            'args': json.dumps(args),
        })
        r = r.json()
        return r['result'][0]

