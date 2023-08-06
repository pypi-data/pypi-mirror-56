import json
import re

from apigateway.event import Event


class Request:
    """ turn api gateway request to flask request"""

    def __init__(self, event: Event, urlpatterns=None, db=None):
        """use lambda event to build flask format request"""
        # url is relative not absolute,different from flask
        self.event = event
        self.url = self.event.data.get("path")
        self.method = self.event.data.get("httpMethod", "GET")
        self.user = None
        self.headers = self.event.headers
        self.body = self.event.body
        self.path = {}
        self.args = self.event.data.get("queryStringParameters")
        self.urlpatterns = urlpatterns
        self.db = db

    def get_data(self):
        """get data from request body,then turn it to json string"""
        return json.dumps(self.body)

    def route(self):
        """match urlpatterns and get flask response."""
        for path in self.urlpatterns:
            # match url
            router = re.match(path['path'], self.url)
            if router:
                self.path = router.groupdict()
                # pass request and path
                self.path['request'] = self
                flask_response = path['view'](self).dispatch(**self.path)
                break
        else:
            flask_response = {'error': 'something wrong in url'}, 400
        return flask_response
