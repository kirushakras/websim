import json
from collections import namedtuple
from .endpoint import WQApiEndpoint


AlphasOverview = namedtuple('AlphasOverview', ['NumFailedAlphas', 'NumOSAlphas', 'NumProdAlphas', 'NumTotalAlphas'])

AlphaData = namedtuple('AlphaData', ["AlphaClientId", "Code", "IsInOS", "Hidden", "IsTeamAlpha", "Favorite", "AlphaName", "CodeType", "DateCreated", "Color", "Region", "Universe", "Sharpe", "Returns", "TurnOver", "Margin"])
AlphaData.__new__.__defaults__ = (None,) * len(AlphaData._fields)


class WQMyAlphas(WQApiEndpoint):
    def alphasoverview(self):
        r = self.do_get('https://www.worldquantvrc.com/myalphas/alphasoverview')
        return AlphasOverview(**r.json()[0])

    def alphadata(self, page=1, limit=40, region=None, universe=None):
        clauses = []
        if region is not None:
            clauses.append({"Region":["{,}",region]})
        if universe is not None:
            clauses.append({"Universe":["{,}",universe]})

        fields = ["LongCount", "Returns","Color","Universe","CodeType","AlphaName","Hidden","Code","Margin","TurnOver","IsInOS","Region","IsTeamAlpha","DateCreated","Sharpe","Favorite"]
        limit = {"limit":limit,"pageNumber":page}
        sort = {"colName":"DateCreated","sortOrder":"DESC"}

        r = self.do_post('https://www.worldquantvrc.com/myalphas/alphadata', data={
            'type': 'is',
            #'_xsrf': XSRF_TOKEN,
            'fields': json.dumps(fields),
            'clauses': json.dumps(clauses),
            'limit': json.dumps(limit),
            'sort': json.dumps(sort),
        }, headers={
            'Content-Type': 'application/x-www-form-urlencoded',
        })
        
        
        result = r.json()
        return (AlphaData(**entry) for entry in result['data'])
        
    def alphainfo(self, alpha_id):
        r = self.do_post('https://www.worldquantvrc.com/alphainfo', data={
            "args": json.dumps({
                "alpha_list": [alpha_id],
            })
        })

        result = r.json()
        return result['result']['alphaInfo']
