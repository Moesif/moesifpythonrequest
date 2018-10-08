# Import libraries
from moesifapi.moesif_api_client import APIHelper
from datetime import datetime


class UtilityFunction():
    # Function to get the current time
    def get_current_time(self):
        return datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3]

    # Function to check if the event is to Moesif
    def is_moesif(self, request_headers, url):
        if request_headers and isinstance(request_headers, dict):
            if request_headers.get('X-Moesif-SDK', None) is not None or request_headers.get('X-Moesif-Application-Id', None) is not None:
                return True

        if url and 'moesif.net' in url:
            return True

        return False

    # Function to mask the body
    def mask_body(self, body, masks):
        """
        recursively removes any element from body (dictionary or lists) that
        have key matches masks. Note, this function have a side effect.
        Please make a deepcopy before using.
        """
        if body is None:
            return body
        if masks is None:
            return body

        if type(body) == list:
            return [self.mask_body(element, masks) for element in body]

        if type(body) == dict:
            for mask in masks:
                body.pop(mask, None)
            for key in body:
                body[key] = self.mask_body(body[key], masks)
            return body

        return body

    # Function to flatten value to string
    def flatten_to_string(self, value):
        if type(value) == str:
            return value
        if value is None:
            return ''
        return APIHelper.json_serialize(value)


    # Function to create request headers
    def create_request_headers(self, req_headers):
        try:
            req_headers = {k: v for k, v in req_headers.items()}
        except:
            req_headers = {}
        return req_headers
