# Import Libraries
from .. import global_variables
from ..patch_request.patch_request import PatchRequest
from ..send_moesif.send_moesif import SendMoesif


class StartCapture():

    # Start capturing the outgoing requests
    def start_capture_outgoing(self, options):

        # Check if the moesif_options are of dict type
        global_variables.moesif_options = options
        global_variables.DEBUG = global_variables.moesif_options.get('LOCAL_DEBUG', False)

        if global_variables.MOESIF_PATCH:
            print('Already started patching the outgoing requests')
        else:
            print('Starting to patch the outgoing requests')

            global_variables.MOESIF_PATCH = True
            # Create an instance of the class
            patch_instance = PatchRequest()
            send_async = SendMoesif()

            _unpatch = patch_instance.patch(send_async.send_moesif_async)
