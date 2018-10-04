# Import libraries
from ..utility_function.utility_function import UtilityFunction
from .. import global_variables
import base64
import json


class DataPreparation():

    # Function to base64 encode data
    def base64_encode(self, data):
        try:
            if global_variables.DEBUG:
                print("about to parse request body as base64")
            encoded_body = base64.standard_b64encode(data)
            transfer_encoding = 'base64'
            if global_variables.DEBUG:
                print("base64 encoded body: " + encoded_body)
        except:
            if global_variables.DEBUG:
                print("Request body is of type other than json or base64")
            encoded_body = None
            transfer_encoding = None

        return encoded_body, transfer_encoding

    # Function to prepare the data
    def transform_data(self, method, url, start_time, end_time, response, kwargs):

        # Create an instance of the class
        utility_function = UtilityFunction()

        if not dict(response.headers):
            rsp_headers = {}
        else:
            rsp_headers = dict(response.headers)

        if kwargs.get('data', None):
            try:
                if global_variables.DEBUG:
                    print("about to parse request data as json")
                req_body = json.loads(json.dumps(kwargs.get('data', None)))
                if global_variables.DEBUG:
                    print("Req body data parsed successfully")
                req_body = utility_function.mask_body(req_body, global_variables.moesif_options.get('REQUEST_BODY_MASKS'))
                req_body_transfer_encoding = 'json'
            except:
                req_body, req_body_transfer_encoding = self.base64_encode(json.dumps(kwargs.get('data', None)))
        elif kwargs.get('json', None):
            try:
                if global_variables.DEBUG:
                    print('about to parse request json')
                req_body = json.loads(kwargs.get('json', None))
                if global_variables.DEBUG:
                    print("Req body json parsed successfully")
                req_body = utility_function.mask_body(req_body, global_variables.moesif_options.get('REQUEST_BODY_MASKS'))
                req_body_transfer_encoding = 'json'
            except:
                req_body, req_body_transfer_encoding = self.base64_encode(kwargs.get('json', None))
        else:
            req_body = None
            req_body_transfer_encoding = None

        req_headers = {k: utility_function.flatten_to_string(v) for k, v in kwargs.get('headers', {}).items()}

        if response.content:
            try:
                if global_variables.DEBUG:
                    print("about to process response body as json")
                rsp_body = json.loads(response.content)
                if global_variables.DEBUG:
                    print("Resp body json parsed succesfully")
                rsp_body = utility_function.mask_body(rsp_body, global_variables.moesif_options.get('RESPONSE_BODY_MASKS'))
                rsp_body_transfer_encoding = 'json'
            except:
                try:
                    if global_variables.DEBUG:
                        print("about to process response body as base64")
                    rsp_body = base64.standard_b64encode(response.content)
                    rsp_body_transfer_encoding = 'base64'
                    if global_variables.DEBUG:
                        print("base64 encoded body: " + rsp_body)
                except:
                    rsp_body = None
                    rsp_body_transfer_encoding = None
        else:
            rsp_body = None
            rsp_body_transfer_encoding = None

        event_model = {
            'request': {
                'time': start_time,
                'uri': url,
                'verb': method,
                'ip_address': None,
                'headers': req_headers,
                'body': req_body,
                'api_version': global_variables.moesif_options.get('API_VERSION', None),
                'transfer_encoding': req_body_transfer_encoding
            },
            'response': {
                'time': end_time,
                'status': response.status_code,
                'headers': rsp_headers,
                'body': rsp_body,
                'transfer_encoding': rsp_body_transfer_encoding
            }
        }

        return event_model
