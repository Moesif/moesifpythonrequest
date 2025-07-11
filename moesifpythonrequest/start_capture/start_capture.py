# Import Libraries
from .. import global_variables as gv
from ..patch_request.patch_request import PatchRequest
from ..send_moesif.send_moesif import SendMoesif
from moesifapi.app_config import AppConfig
from moesifapi.moesif_api_client import MoesifAPIClient, Configuration
import logging

logger = logging.getLogger(__name__)

class StartCapture():

    # Start capturing the outgoing requests
    def start_capture_outgoing(self, options):

        # Check if the moesif_options are of dict type
        gv.moesif_options = options
        gv.DEBUG = gv.moesif_options.get('LOCAL_DEBUG', False)

        if gv.MOESIF_PATCH:
            logger.info('Already started patching the outgoing requests')
        else:
            logger.info('Starting to patch the outgoing requests')

            gv.MOESIF_PATCH = True
            # Create an instance of the class
            patch_instance = PatchRequest()
            send_async = SendMoesif()
            gv.app_config = AppConfig()

            if gv.DEBUG:
                Configuration.BASE_URI = gv.moesif_options.get('LOCAL_MOESIF_BASEURL', 'https://api.moesif.net')

            # Get the MoesifAPI client
            if gv.moesif_options.get('APPLICATION_ID', None):
                gv.api_client = MoesifAPIClient(gv.moesif_options.get('APPLICATION_ID')).api
            else:
                raise Exception('Moesif Application ID is required in moesif options')

            # Get the application config
            gv.config = gv.app_config.get_config(gv.api_client, gv.DEBUG)

            # Parse the application config
            try:
                if gv.config:
                    gv.config_etag, gv.sampling_percentage, gv.last_updated_time = gv.app_config.parse_configuration(
                        gv.config, gv.DEBUG)
            except:
                if gv.DEBUG:
                    logger.info('Error while parsing application configuration on initialization')

            _unpatch = patch_instance.patch(send_async.send_moesif_async)
