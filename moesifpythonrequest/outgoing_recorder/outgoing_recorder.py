# Import Libraries
from moesifapi.models import EventModel
from collections import namedtuple
from .. import global_variables
import urlparse


class OutgoingRecorder():
    # Function to transform the request headers
    def transform_key(self, key):
        key = key.upper()
        key = key.replace('-', '_')
        return key

    # Function to create request headers
    def create_request_headers(self,req_headers):
        try:
            req_headers = {self.transform_key(k): v for k, v in req_headers.items()}
        except:
            req_headers = {}
        return req_headers

    # Function to mock the requests as Django Request and Response object
    def create_mock_request_response(self, event_model):

        fake_django_incoming_request = {
            'mo_mocked': True,
            'method': event_model['request']['verb'],
            'url': event_model['request']['uri'],
            'path': urlparse.urlparse(event_model['request']['uri']).path,
            'META': self.create_request_headers(event_model['request']['headers']),
            'body': event_model['request']['body']
        }

        fake_django_incoming_response = {
            'mo_mocked': True,
            'statusCode': event_model['response']['status'],
            'content': event_model['response']['body']
        }

        fake_request = namedtuple("fake_request", fake_django_incoming_request.keys())(
            *fake_django_incoming_request.values())
        fake_response = namedtuple("fake_response", fake_django_incoming_response.keys())(
            *fake_django_incoming_response.values())

        return fake_request, fake_response

    # Function to prepare the recorder
    def prepare_recorder(self, options, event_model):
        mock_req, mock_res = self.create_mock_request_response(event_model)

        try:
            identify_user = options.get('IDENTIFY_USER', None)
            if identify_user is not None:
                event_model['user_id'] = identify_user(mock_req, mock_res)
        except:
            event_model['user_id'] = None
            if global_variables.DEBUG:
                print("can not execute identify_user function, Please check moesif settings.")

        try:
            get_session_token = options.get('GET_SESSION_TOKEN', None)
            if get_session_token is not None:
                event_model['session_token'] = get_session_token(mock_req, mock_res)
        except:
            event_model['session_token'] = None
            if global_variables.DEBUG:
                print("Can not execute get_session_token function. Please check moesif settings.")

        try:
            get_metadata = options.get('GET_METADATA', None)
            if get_metadata is not None:
                event_model['metadata'] = get_metadata(mock_req, mock_res)
        except:
            event_model['metadata'] = None
            if global_variables.DEBUG:
                print("can not execute get_metadata function, please check moesif settings.")

        try:
            skip_event = options.get('SKIP', None)
            if skip_event is not None:
                if skip_event(mock_req, mock_res):
                    return mock_res
        except:
            if global_variables.DEBUG:
                print("Having difficulty executing skip_event function. Please check moesif settings.")

        return EventModel().from_dictionary(event_model)
