import requests
from copy import deepcopy

from chargebee_byte.requests import SubscriptionRequest, CustomerRequest


class Client(object):
    def __init__(self, site, api_key):
        self.auth = requests.auth.HTTPBasicAuth(api_key, '')
        self.api_url = 'https://{}.chargebee.com/api/v2'.format(site)

    def _get_paginated_objects(self, request):
        response = requests.get(self.api_url + request.path, auth=self.auth, params=request.data)
        response.raise_for_status()
        return response.json()

    def _get_all_objects(self, paginated_func, parameters):
        ret = {'next_offset': ''}
        objects = []

        while 'next_offset' in ret:
            new_parameters = deepcopy(parameters) or {}
            new_parameters['offset'] = ret['next_offset']
            ret = paginated_func(new_parameters)
            objects += ret['list']

        return objects

    def get_paginated_subscriptions(self, parameters=None):
        return self._get_paginated_objects(SubscriptionRequest(parameters))

    def get_all_subscriptions(self, parameters=None):
        return self._get_all_objects(self.get_paginated_subscriptions, parameters)

    def get_paginated_customers(self, parameters=None):
        return self._get_paginated_objects(CustomerRequest(parameters))

    def get_all_customers(self, parameters=None):
        return self._get_all_objects(self.get_paginated_customers, parameters)
