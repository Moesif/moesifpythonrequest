# Import Libraries
from moesifapi.models import EventModel
from collections import namedtuple
from .. import global_variables
import base64
import json
from ..utility_function.utility_function import UtilityFunction


class OutgoingRecorder():

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

    # Function to prepare the event_model
    def prepare_model(self, mock_req, mock_res, event_model, start_time, end_time):

        # Create an instance of the class
        utility_function = UtilityFunction()

        if mock_req.body:
            try:
                if global_variables.DEBUG:
                    print('about to parse request json')
                req_body = json.loads(mock_req.body)
                if global_variables.DEBUG:
                    print("Req body json parsed successfully")
                req_body = utility_function.mask_body(req_body, global_variables.moesif_options.get('REQUEST_BODY_MASKS'))
                req_body_transfer_encoding = 'json'
            except:
                req_body, req_body_transfer_encoding = self.base64_encode(mock_req.body)
        else:
            req_body = None
            req_body_transfer_encoding = None

        if mock_res.content:
            try:
                if global_variables.DEBUG:
                    print("about to process response body as json")
                rsp_body = json.loads(mock_res.content)
                if global_variables.DEBUG:
                    print("Resp body json parsed successfully")
                rsp_body = utility_function.mask_body(rsp_body, global_variables.moesif_options.get('RESPONSE_BODY_MASKS'))
                rsp_body_transfer_encoding = 'json'
            except:
                rsp_body, rsp_body_transfer_encoding = self.base64_encode(mock_res.content)
        else:
            rsp_body = None
            rsp_body_transfer_encoding = None

        mo_model = {
            'request': {
                'time': start_time,
                'uri': mock_req.url,
                'verb': mock_req.method,
                'api_version': global_variables.moesif_options.get('API_VERSION', None),
                'ip_address': None,
                'headers': utility_function.create_request_headers(mock_req.headers),
                'body': req_body,
                'transfer_encoding': req_body_transfer_encoding
            },
            'response': {
                'time': end_time,
                'status': mock_res.status_code,
                'headers': utility_function.create_request_headers(mock_res.headers),
                'body': rsp_body,
                'transfer_encoding': rsp_body_transfer_encoding
            },
            'session_token': event_model['session_token'],
            'user_id': event_model['user_id'],
            'metadata': event_model['metadata']
        }

        return mo_model

    # Function to prepare the recorder
    def prepare_recorder(self, options, mock_req, mock_res, start_time, end_time):

        event_model = {}
        event_model['user_id'] = None
        try:
            identify_user = options.get('IDENTIFY_USER_OUTGOING', None)
            if identify_user is not None:
                event_model['user_id'] = identify_user(mock_req, mock_res)
        except:
            if global_variables.DEBUG:
                print("can not execute identify_user function, Please check moesif settings.")

        event_model['session_token'] = None
        try:
            get_session_token = options.get('GET_SESSION_TOKEN_OUTGOING', None)
            if get_session_token is not None:
                event_model['session_token'] = get_session_token(mock_req, mock_res)
        except:
            if global_variables.DEBUG:
                print("Can not execute get_session_token function. Please check moesif settings.")

        event_model['metadata'] = None
        try:
            get_metadata = options.get('GET_METADATA_OUTGOING', None)
            if get_metadata is not None:
                event_model['metadata'] = get_metadata(mock_req, mock_res)
        except:
            if global_variables.DEBUG:
                print("can not execute get_metadata function, please check moesif settings.")

        try:
            skip_event = options.get('SKIP_OUTGOING', None)
            if skip_event is not None:
                if skip_event(mock_req, mock_res):
                    return mock_res
        except:
            if global_variables.DEBUG:
                print("Having difficulty executing skip_event function. Please check moesif settings.")

        # Prepare the moesif model
        mo_model = self.prepare_model(mock_req, mock_res, event_model, start_time, end_time)
        return EventModel().from_dictionary(mo_model)
