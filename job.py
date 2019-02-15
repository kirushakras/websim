from ..exceptions import WQJobProgressError
from .endpoint import WQApiEndpoint


class WQJobClient(WQApiEndpoint):
    def details(self, jobid):
        r = self.do_post('https://www.worldquantvrc.com/job/details/' + str(jobid))
        return r.json()

    def progress(self, jobid):
        r = self.do_post('https://www.worldquantvrc.com/job/progress/' + str(jobid))
        progress = r.json()
        if progress == 'DONE':
            return 100
        if progress == 'ERROR':
            raise WQJobProgressError('Job ' + str(jobid) + ' has been stopped with error')
        return int(progress)

    def error(self, jobid):
        r = self.do_post('https://www.worldquantvrc.com/job/error/' + str(jobid))
        return r.json()

