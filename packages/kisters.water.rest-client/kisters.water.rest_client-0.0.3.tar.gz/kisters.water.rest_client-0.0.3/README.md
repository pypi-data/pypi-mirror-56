# Kisters REST Client Library

This library allows connections to Kisters servers. It supports authentication
with OpenID Connect.

## Installation

Install with `pip`:

```bash
> python -m pip install kisters.water.rest_client
```


## Example Usage

```python
from kisters.water.rest_client import RESTClient
from kisters.water.rest_client.auth import OpenIDConnect

# Instantiate the authentication class with credentials
authentication = OpenIDConnect(
    client_id="jesse-test",
    client_secret="c4b0f70d-d2e6-497f-b11c-d49fe806c29b",
)
# Instantiate the client class with the service url and authentication
client = RESTClient(
    url="https://jesse-test.hydraulic-network.kisters.cloud",
    authentication=authentication
)
# Verify the client is set up correctly
# Note: If you have not created any networks yet, this could be an empty list
client.get("rest/networks")
# ['my-network', 'my-other-network', ...]
```
