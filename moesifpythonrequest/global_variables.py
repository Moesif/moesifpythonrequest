"""This module is to declare global objects."""
from datetime import datetime

# Configuration Options
global moesif_options
moesif_options = {}

# Debug Flag
global DEBUG
DEBUG = True

# Patch Flag
global MOESIF_PATCH
MOESIF_PATCH = False

# MoesifAPI Client
global api_client
api_client = None

# App Config class
global app_config
app_config = None

# App Config
global config
config = None

# App Config sampling percentage
global sampling_percentage
sampling_percentage = 100

# App Config eTag
global config_etag
config_etag = None

# App Config last updated time
global last_updated_time
last_updated_time = datetime.utcnow()
