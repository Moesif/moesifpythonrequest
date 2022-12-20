# Moesif Python Requests

[![Built For][ico-built-for]][link-built-for]
[![Latest Version][ico-version]][link-package]
[![Language Versions][ico-language]][link-language]
[![Software License][ico-license]][link-license]
[![Source Code][ico-source]][link-source]

Interceptor for Python Requests lib to capture _outgoing_ API calls and sends to [Moesif](https://www.moesif.com) for API analytics and monitoring.

_If you are using Moesif's API monitoring SDKs like [Moesif Django](https://github.com/Moesif/moesifdjango) or [Moesif WSGI](https://github.com/moesif/moesifwsgi) to log incoming API calls, this library is already included._

## How to install

```shell
pip install moesifpythonrequest
```

Import the Moesif lib and call start_capture_outgoing.
Moesif will start logging all API calls made from the requests lib.

```python
from moesifpythonrequest.start_capture.start_capture import StartCapture
import requests

moesif_settings = {
    'APPLICATION_ID': 'Your Moesif Application Id'
}

def main():
    # Outgoing API call to third party like Github / Stripe or to your own dependencies
    response = requests.get("http://httpbin.org/uuid")
    print(response.json())

StartCapture().start_capture_outgoing(moesif_settings)
main()
```

Your Moesif Application Id can be found in the [_Moesif Portal_](https://www.moesif.com/).
After signing up for a Moesif account, your Moesif Application Id will be displayed during the onboarding steps.

## Configuration options

### __`APPLICATION_ID`__

(required) _string_, Your Moesif Application Id which can be found by logging
into the [_Moesif Portal_](https://www.moesif.com/), click on the top right menu,
and then clicking _Installation_.

### __`GET_METADATA_OUTGOING`__

(optional) _(req, res) => dictionary_, a function that enables you to return custom metadata associated with the logged API calls.
Takes in the [Requests](http://docs.python-requests.org/en/master/api/) request and response object as arguments. You should implement a function that
returns a dictionary containing your custom metadata. (must be able to be encoded into JSON). For example, you may want to save a VM instance_id, a trace_id, or a resource_id with the request.

### __`IDENTIFY_USER_OUTGOING`__

(optional, but highly recommended) _(req, res) => string_, a function that takes [Requests](http://docs.python-requests.org/en/master/api/) request and response, and returns a string that is the user id used by your system. While Moesif tries to identify users automatically,
but different frameworks and your implementation might be very different, it would be helpful and much more accurate to provide this function.

### __`IDENTIFY_COMPANY_OUTGOING`__

(optional) _(req, res) => string_, a function that takes [Requests](http://docs.python-requests.org/en/master/api/) request and response, and returns a string that is the company id for this event.

### __`GET_SESSION_TOKEN_OUTGOING`__

(optional) _(req, res) => string_, a function that takes [Requests](http://docs.python-requests.org/en/master/api/) request and response, and returns a string that is the session token for this event. Again, Moesif tries to get the session token automatically, but if you setup is very different from standard, this function will be very help for tying events together, and help you replay the events.

### __`LOG_BODY_OUTGOING`__

(optional) _boolean_, default True, Set to False to remove logging request and response body.

### __`SKIP_OUTGOING`__

(optional) _(req, res) => boolean_, a function that takes a [Requests](http://docs.python-requests.org/en/master/api/) request and response,
and returns true if you want to skip this particular event.

### __`MASK_EVENT_MODEL`__

(optional) _(EventModel) => EventModel_, a function that takes a [Moesif EventModel](https://github.com/Moesif/moesifapi-python/blob/master/moesifapi/models/event_model.py) and returns an EventModel with desired data removed. For details regarding EventModel please see the [Moesif Python API Documentation](https://www.moesif.com/docs/api?python).

## Example

An example Moesif integration is [available on GitHub](https://github.com/Moesif/moesif-python-outgoing-example)

## Other integrations

To view more documentation on integration options, please visit __[the Integration Options Documentation](https://www.moesif.com/docs/getting-started/integration-options/).__

[ico-built-for]: https://img.shields.io/badge/built%20for-python%20requests-blue.svg
[ico-version]: https://img.shields.io/pypi/v/moesifpythonrequest.svg
[ico-language]: https://img.shields.io/pypi/pyversions/moesifpythonrequest.svg
[ico-license]: https://img.shields.io/badge/License-Apache%202.0-green.svg
[ico-source]: https://img.shields.io/github/last-commit/moesif/moesifpythonrequest.svg?style=social

[link-built-for]: http://docs.python-requests.org/en/master/
[link-package]: https://pypi.python.org/pypi/moesifpythonrequest
[link-language]: https://pypi.python.org/pypi/moesifpythonrequest
[link-license]: https://raw.githubusercontent.com/Moesif/moesifpythonrequest/master/LICENSE
[link-source]: https://github.com/Moesif/moesifpythonrequest
