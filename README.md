# Moesif for Python Requests
by [Moesif](https://moesif.com), the [API analytics](https://www.moesif.com/features/api-analytics) and [API monetization](https://www.moesif.com/solutions/metered-api-billing) platform.

[![Built For][ico-built-for]][link-built-for]
[![Latest Version][ico-version]][link-package]
[![Language Versions][ico-language]][link-language]
[![Software License][ico-license]][link-license]
[![Source Code][ico-source]][link-source]

It's an interceptor for Python Requests library that captures outgoing API calls and sends to [Moesif](https://www.moesif.com) for API analytics and monitoring.

> If you're new to Moesif, see [our Getting Started](https://www.moesif.com/docs/) resources to quickly get up and running.

> If you are using Moesif's API monitoring SDKs like [Moesif Django](https://github.com/Moesif/moesifdjango) or [Moesif WSGI](https://github.com/moesif/moesifwsgi) to log incoming API calls, this library is already included.

## Prerequisites
Before using Moesif for Python Requests, make sure you have the following:

- [An active Moesif account](https://moesif.com/wrap)
- [A Moesif Application ID](#get-your-moesif-application-id)

### Get Your Moesif Application ID
After you log into [Moesif Portal](https://www.moesif.com/wrap), you can get your Moesif Application ID during the onboarding steps. You can always access the Application ID any time by following these steps from Moesif Portal after logging in:

1. Select the account icon to bring up the settings menu.
2. Select **Installation** or **API Keys**.
3. Copy your Moesif Application ID from the **Collector Application ID** field.
<img class="lazyload blur-up" src="images/app_id.png" width="700" alt="Accessing the settings menu in Moesif Portal">

## Install
Install with pip:

```shell
pip install moesifpythonrequest
```

## Configure
See the available [configuration options](#configuration-options) to learn how to configure `moesifpythonrequest` for your use case.

## How to Use

Import the Moesif library and call the `start_capture_outgoing` method.
Moesif will start logging all API calls made from the Requests library.

```python
from moesifpythonrequest.start_capture.start_capture import StartCapture
import requests

moesif_settings = {
    'APPLICATION_ID': 'YOUR_MOESIF_APPLICATION_ID'
}

def main():
    # Outgoing API call to third party like Github / Stripe or to your own dependencies
    response = requests.get("http://httpbin.org/uuid")
    print(response.json())

StartCapture().start_capture_outgoing(moesif_settings)
main()
```

Replace *`YOUR_MOESIF_APPLICATION_ID`* with [your Moesif Application ID](#get-your-moesif-application-id).

## Troubleshoot
For a general troubleshooting guide that can help you solve common problems, see [Server Troubleshooting Guide](https://www.moesif.com/docs/troubleshooting/server-troubleshooting-guide/).

Other troubleshooting supports:

- [FAQ](https://www.moesif.com/docs/faq/)
- [Moesif support email](mailto:support@moesif.com)

## Repository Structure

```
.
├── images/
├── LICENSE
├── MANIFEST.in
├── moesifpythonrequest/
├── README.md
├── register.py
├── requirements.txt
├── setup.cfg
└── setup.py
```

## Configuration options
The following sections describe the available configuration options. You have to set these options in a Python dictionary and pass that as an argument as you call the `start_capture_outgoing` method. See the [example](https://github.com/Moesif/moesif-python-outgoing-example/blob/master/main.py#L31) for better understanding.

### `APPLICATION_ID` (Required)
<table>
  <tr>
   <th scope="col">
    Data type
   </th>
  </tr>
  <tr>
   <td>
    String
   </td>
  </tr>
</table>

A string that [identifies your application in Moesif](#get-your-moesif-application-id).

### `GET_METADATA_OUTGOING`
table>
  <tr>
   <th scope="col">
    Data type
   </th>
   <th scope="col">
    Parameters
   </th>
   <th scope="col">
    Return type
   </th>
  </tr>
  <tr>
   <td>
    Function
   </td>
   <td>
    <code>(req, res)</code>
   </td>
   <td>
    Dictionary
   </td>
  </tr>
</table>

Optional.

A function that enables you to return custom metadata associated with the logged API calls.

Takes in the [Requests](http://docs.python-requests.org/en/master/api/) request and response objects as arguments. 

We recommend that you implement a function that
returns a dictionary containing your custom metadata. The dictionary must be a valid one that can be encoded into JSON. For example, you may want to save a virtual machine instance ID, a trace ID, or a resource ID with the request.

### `IDENTIFY_USER_OUTGOING`
<table>
  <tr>
   <th scope="col">
    Data type
   </th>
   <th scope="col">
    Parameters
   </th>
   <th scope="col">
    Return type
   </th>
  </tr>
  <tr>
   <td>
    Function
   </td>
   <td>
    <code>(req, res)</code>
   </td>
   <td>
    String
   </td>
  </tr>
</table>

Optional, but highly recommended.

A function that takes [Requests](http://docs.python-requests.org/en/master/api/) request and response objects, and returns a string that represents the user ID used by your system. 

While Moesif tries to identify users automatically, different frameworks and your implementation might vary. So we highly recommend that you accurately provide a 
user ID using this function.

### `IDENTIFY_COMPANY_OUTGOING`
<table>
  <tr>
   <th scope="col">
    Data type
   </th>
   <th scope="col">
    Parameters
   </th>
   <th scope="col">
    Return type
   </th>
  </tr>
  <tr>
   <td>
    Function
   </td>
   <td>
    <code>(req, res)</code>
   </td>
   <td>
    String
   </td>
  </tr>
</table>

Optional.

A function that takes [Requests](http://docs.python-requests.org/en/master/api/) request and response objects and returns a string that represents the company ID for this event.


### `GET_SESSION_TOKEN_OUTGOING`
<table>
  <tr>
   <th scope="col">
    Data type
   </th>
   <th scope="col">
    Parameters
   </th>
   <th scope="col">
    Return type
   </th>
  </tr>
  <tr>
   <td>
    Function
   </td>
   <td>
    <code>(req, res)</code>
   </td>
   <td>
    String
   </td>
  </tr>
</table>

Optional.

A function that takes [Requests](http://docs.python-requests.org/en/master/api/) request and response objects, and returns a string that corresponds to the session token for this event. 

Similar to [user IDs](#identify_user_outgoing), Moesif tries to get the session token automatically. However, if you setup differs from the standard, this function can help tying up events together and help you replay the events.

### `LOG_BODY_OUTGOING`
<table>
  <tr>
   <th scope="col">
    Data type
   </th>
   <th scope="col">
    Default
   </th>
  </tr>
  <tr>
   <td>
    Boolean
   </td>
   <td>
    <code>True</code>
   </td>
  </tr>
</table>

Optional.

Set to `False` to remove logging request and response body.

### `SKIP_OUTGOING`
<table>
  <tr>
   <th scope="col">
    Data type
   </th>
   <th scope="col">
    Parameters
   </th>
   <th scope="col">
    Return type
   </th>
  </tr>
  <tr>
   <td>
    Function
   </td>
   <td>
    <code>(req, res)</code>
   </td>
   <td>
    Boolean
   </td>
  </tr>
</table>

Optional.

A function that takes a [Requests](http://docs.python-requests.org/en/master/api/) request and response objects,
and returns `True` if you want to skip this particular event.

### `MASK_EVENT_MODEL`
<table>
  <tr>
   <th scope="col">
    Data type
   </th>
   <th scope="col">
    Parameters
   </th>
   <th scope="col">
    Return type
   </th>
  </tr>
  <tr>
   <td>
    Function
   </td>
   <td>
    <code>(EventModel)</code>
   </td>
   <td>
    <code>EventModel</code>
   </td>
  </tr>
</table>

Optional.

A function that takes the final Moesif event model and returns an `EventModel` object with desired data removed.

For more information about Moesif event model, see [Moesif Python API documentation](https://www.moesif.com/docs/api?python).

## Examples

An example Moesif integration is [available on GitHub](https://github.com/Moesif/moesif-python-outgoing-example).

## How to Get Help
If you face any issues, try the [troubheshooting guidelines](#troubleshoot). For further assistance, reach out to our [support team](mailto:support@moesif.com).

## Explore Other Integrations

Explore other integration options from Moesif:

- [Server integration options documentation](https://www.moesif.com/docs/server-integration//)
- [Client integration options documentation](https://www.moesif.com/docs/client-integration/)

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
