# Import Libraries
from moesifapi.exceptions.api_exception import APIException
from moesifapi.moesif_api_client import MoesifAPIClient, Configuration
from .. import global_variables
import threading


class SendMoesif():
    # Function to send event to Moesif
    def send_event(self, application_id, event_model):
        if global_variables.moesif_options.get('LOCAL_DEBUG', False):
            Configuration.BASE_URI = global_variables.moesif_options.get('LOCAL_MOESIF_BASEURL', 'https://api.moesif.net')

        client = MoesifAPIClient(application_id)
        api_client = client.api
        try:
            if global_variables.DEBUG:
                print('Calling API to create event')
            api_client.create_event(event_model)
            if global_variables.DEBUG:
                print("sent done")
        except APIException as inst:
            if 401 <= inst.response_code <= 403:
                print("Unauthorized access sending event to Moesif. Please check your Appplication Id.")
            if global_variables.DEBUG:
                print("Error sending event to Moesif, with status code:")
                print(inst.response_code)

    # Function to send event async
    def send_moesif_async(self, applicaiton_id, event_model):
        try:
            mask_event_model = global_variables.moesif_options.get('MASK_EVENT_MODEL', None)
            if mask_event_model is not None:
                if global_variables.DEBUG:
                    print('Masking the event')
                event_model = mask_event_model(event_model)
        except:
            if global_variables.DEBUG:
                print("Can not execute MASK_EVENT_MODEL function. Please check moesif settings.")

        sending_background_thread = threading.Thread(target=self.send_event, args=(applicaiton_id, event_model,))
        if global_variables.DEBUG:
            print('Staring a new thread')
        sending_background_thread.start()
