# Import Libraries
from moesifapi.models import EventModel
from ..utility_function.utility_function import UtilityFunction
from ..outgoing_recorder.outgoing_recorder import OutgoingRecorder
import requests
from .. import global_variables


class PatchRequest():
    # Function to patch the outgoing requests
    def patch(self, recorder):
        old_request_function = requests.request
        old_get_function = requests.get
        old_options_function = requests.options
        old_head_function = requests.head
        old_post_function = requests.post
        old_put_function = requests.put
        old_patch_function = requests.patch
        old_delete_function = requests.delete

        # Patch the requests function
        def new_request_function(method, url, **kwargs):
            # Create an instance of the Outgoing Recorder class
            outgoing_recorder = OutgoingRecorder()
            utility_function = UtilityFunction()

            start_time = utility_function.get_current_time()
            response = old_request_function(method, url, **kwargs)
            end_time = utility_function.get_current_time()

            if not utility_function.is_moesif(kwargs.get('headers', None), url):
                generated_recorder = outgoing_recorder.prepare_recorder(global_variables.moesif_options, response.request, response, start_time, end_time)

                if isinstance(generated_recorder, EventModel):
                    moesif_response = recorder(global_variables.moesif_options.get('APPLICATION_ID'), generated_recorder)

            return response

        def new_get_function(url, params=None, **kwargs):
            r"""Sends a GET request.
            :param url: URL for the new :class:`Request` object.
            :param params: (optional) Dictionary or bytes to be sent in the query string for the :class:`Request`.
            :param \*\*kwargs: Optional arguments that ``request`` takes.
            :return: :class:`Response <Response>` object
            :rtype: requests.Response
            """

            kwargs.setdefault('allow_redirects', True)
            return requests.request('get', url, params=params, **kwargs)

        def new_options_function(url, **kwargs):
            r"""Sends an OPTIONS request.
            :param url: URL for the new :class:`Request` object.
            :param \*\*kwargs: Optional arguments that ``request`` takes.
            :return: :class:`Response <Response>` object
            :rtype: requests.Response
            """

            kwargs.setdefault('allow_redirects', True)
            return requests.request('options', url, **kwargs)

        def new_head_function(url, **kwargs):
            r"""Sends a HEAD request.
            :param url: URL for the new :class:`Request` object.
            :param \*\*kwargs: Optional arguments that ``request`` takes.
            :return: :class:`Response <Response>` object
            :rtype: requests.Response
            """

            kwargs.setdefault('allow_redirects', False)
            return requests.request('head', url, **kwargs)

        def new_post_function(url, data=None, json=None, **kwargs):
            r"""Sends a POST request.
            :param url: URL for the new :class:`Request` object.
            :param data: (optional) Dictionary (will be form-encoded), bytes, or file-like object to send in the body of the :class:`Request`.
            :param json: (optional) json data to send in the body of the :class:`Request`.
            :param \*\*kwargs: Optional arguments that ``request`` takes.
            :return: :class:`Response <Response>` object
            :rtype: requests.Response
            """

            return requests.request('post', url, data=data, json=json, **kwargs)

        def new_put_function(url, data=None, **kwargs):
            r"""Sends a PUT request.
            :param url: URL for the new :class:`Request` object.
            :param data: (optional) Dictionary (will be form-encoded), bytes, or file-like object to send in the body of the :class:`Request`.
            :param json: (optional) json data to send in the body of the :class:`Request`.
            :param \*\*kwargs: Optional arguments that ``request`` takes.
            :return: :class:`Response <Response>` object
            :rtype: requests.Response
            """

            return requests.request('put', url, data=data, **kwargs)

        def new_patch_function(url, data=None, **kwargs):
            r"""Sends a PATCH request.
            :param url: URL for the new :class:`Request` object.
            :param data: (optional) Dictionary (will be form-encoded), bytes, or file-like object to send in the body of the :class:`Request`.
            :param json: (optional) json data to send in the body of the :class:`Request`.
            :param \*\*kwargs: Optional arguments that ``request`` takes.
            :return: :class:`Response <Response>` object
            :rtype: requests.Response
            """

            return requests.request('patch', url, data=data, **kwargs)

        def new_delete_function(url, **kwargs):
            r"""Sends a DELETE request.
            :param url: URL for the new :class:`Request` object.
            :param \*\*kwargs: Optional arguments that ``request`` takes.
            :return: :class:`Response <Response>` object
            :rtype: requests.Response
            """

            return requests.request('delete', url, **kwargs)

            # Actual patch

        # Actual Patch
        requests.request = new_request_function
        requests.get = new_get_function
        requests.options = new_options_function
        requests.head = new_head_function
        requests.post = new_post_function
        requests.put = new_put_function
        requests.patch = new_patch_function
        requests.delete = new_delete_function

        # Function to unpatch the requests
        def _unpatch():
            requests.request = old_request_function
            requests.get = old_get_function
            requests.options = old_options_function
            requests.head = old_head_function
            requests.post = old_post_function
            requests.put = old_put_function
            requests.patch = old_patch_function
            requests.delete = old_delete_function

        return _unpatch
