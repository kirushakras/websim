from .endpoint import WQApiEndpoint
import json

class WQSubmissionClient(WQApiEndpoint):
    def check(alpha_id):
        r = self.do_post('https://www.worldquantvrc.com/submission/check', data={
            "args": json.dumps({
                "alpha_list": [alpha_id],
            })
        })
        return r.json()['result']['RequestId']

    def result(self, jobid):
        r = self.do_post('https://www.worldquantvrc.com/submission/result/' + str(jobid))
        r = r.json()['Result']
        return (r['InProgress'], r['response'])

    def start(self, alpha_id):
        r = self.do_post('https://www.worldquantvrc.com/submission/start', data={
            "args": json.dumps({
                "alpha_list": [alpha_id],
            })
        })
        return r.json()['result']['RequestId']
    
