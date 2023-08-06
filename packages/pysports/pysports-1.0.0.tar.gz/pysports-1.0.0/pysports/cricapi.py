import requests
from pysports.credentials import Credentials


class CricAPI(Credentials):
    def __init__(self, *args):
        super(CricAPI, self).__init__(*args)

    def upcoming_matches(self):
        url_endpoint = "matches/"
        url = self.url + url_endpoint
        curl = url + "?apikey=" + self.apikey
        req = requests.get(curl)
        data = req.json()
        return data

    def historical_matches(self):
        url_endpoint = "cricket/"
        url = self.url + url_endpoint
        curl = url + "?apikey=" + self.apikey
        req = requests.get(curl)
        data = req.json()
        return data

    def match_summary(self, match_id):
        url_endpoint = "fantasySummary/"
        url = self.url + url_endpoint
        curl = str(url) + "?apikey=" + str(self.apikey) + "&unique_id=" + str(match_id)
        req = requests.get(curl)
        data = req.json()
        return data

    def live_score(self, match_id):
        url_endpoint = "cricketScore/"
        url = self.url + url_endpoint
        curl = str(url) + "?apikey=" + str(self.apikey) + "&unique_id=" + str(match_id)
        req = requests.get(curl)
        data = req.json()
        return data

    def about_player(self, player_id):
        url_endpoint = "playerStats/"
        url = self.url + url_endpoint
        curl = str(url) + "?apikey=" + str(self.apikey) + "&pid=" + str(player_id)
        req = requests.get(curl)
        data = req.json()
        return data
