# Import Libraries
from moesifapi.exceptions.api_exception import APIException
from .. import global_variables as gv
from datetime import datetime, timedelta
import threading
import random
import math


class SendMoesif():
    # Function to send event to Moesif
    def send_event(self, event_model):
        try:
            if gv.DEBUG:
                print('Calling API to create event')
            event_api_response = gv.api_client.create_event(event_model)
            event_response_config_etag = event_api_response.get("X-Moesif-Config-ETag")

            if event_response_config_etag is not None \
                    and gv.config_etag is not None \
                    and gv.config_etag != event_response_config_etag \
                    and datetime.utcnow() > gv.last_updated_time + timedelta(minutes=5):
                try:
                    gv.config = gv.app_config.get_config(gv.api_client, gv.DEBUG)
                    self.config_etag, self.sampling_percentage, self.last_updated_time = gv.app_config.parse_configuration(
                        gv.config, gv.DEBUG)
                except:
                    if gv.DEBUG:
                        print('Error while updating the application configuration')
            if gv.DEBUG:
                print("Event sent successfully")
        except APIException as inst:
            if 401 <= inst.response_code <= 403:
                print("Unauthorized access sending event to Moesif. Please check your Appplication Id.")
            if gv.DEBUG:
                print("Error sending event to Moesif, with status code:")
                print(inst.response_code)

    # Function to send event async
    def send_moesif_async(self, event_model):
        try:
            mask_event_model = gv.moesif_options.get('MASK_EVENT_MODEL', None)
            if mask_event_model is not None:
                if gv.DEBUG:
                    print('Masking the event')
                event_model = mask_event_model(event_model)
        except:
            if gv.DEBUG:
                print("Can not execute MASK_EVENT_MODEL function. Please check moesif settings.")

        random_percentage = random.random() * 100
        gv.sampling_percentage = gv.app_config.get_sampling_percentage(event_model, gv.config, event_model.user_id, event_model.company_id)

        if gv.sampling_percentage >= random_percentage:
            event_model.weight = 1 if gv.sampling_percentage == 0 else math.floor(100 / gv.sampling_percentage)
            sending_background_thread = threading.Thread(target=self.send_event, args=(event_model,))
            if gv.DEBUG:
                print('Staring a new thread')
            sending_background_thread.start()
        else:
            if gv.DEBUG:
                print('Skipped Event due to sampling percentage: ' + str(
                    gv.sampling_percentage) + ' and random percentage: ' + str(random_percentage))
