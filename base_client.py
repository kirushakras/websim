from threading import RLock

import requests

from ..exceptions import WQAuthenticationError


class WQBaseClient(object):
    def __init__(self):
        self.jar = None
        self.email = None
        self.password = None
        self.lock = RLock()

    def do_query(self, *args, **kwargs):
        with self.lock:
            if self.jar is not None:
                if 'cookies' not in kwargs: kwargs['cookies'] = self.jar
                #self.jar['_xsrf'] = XSRF_TOKEN
                #print(kwargs['cookies'])

            kwargs['allow_redirects'] = False
            r = requests.request(*args, **kwargs)

            location = r.headers.get('Location', None)
            is_login_required = location is not None and location.startswith('/login')
            if is_login_required:
                self.login(self.email, self.password)
                return self.do_query(*args, **kwargs)
            #self.jar = r.cookies
            #print('OUT COOKIES', self.jar)
            #print('OK', r.text)
            return r

    def do_post(self, *args, **kwargs):
        return self.do_query('POST', *args, **kwargs)

    def do_get(self, *args, **kwargs):
        return self.do_query('GET', *args, **kwargs)

    def login(self, email, password):
        r = self.do_post('https://www.worldquantvrc.com/login/process', data={
            'EmailAddress': email,
            'Password': password,
            'next': '',
            'g-recaptcha-response': '',
        })

        result = r.json()
        if result['error'] is not None:
            raise WQAuthenticationError(result['error'])

        self.jar = r.cookies
        self.email = email
        self.password = password
