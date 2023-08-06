# Provides user and api credential.
class Credentials(object):
    def __init__(self, apikey):
        self.url = "http://cricapi.com/api/"
        self.apikey = apikey

    def url_detail(self):
        return dict(url=self.url)

    def apikey_detail(self):
        return dict(apikey=self.apikey)