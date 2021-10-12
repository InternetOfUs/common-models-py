# WeNet - Common models Library

This repository contains some common classes used in Wenet projects.


## Models

The library defines models that describe:

- users
- tasks and transactions
- norms
- messages from the WeNet platform to the applications
- app
- messages for logging

## Component interfaces

The library also provides interfaces for simplifying the communication with the various component of the WeNet platform.

* Service APIs
* Hub
* Incentive Server
* Logging component
* Task Manager
* Profile Manager

Such interfaces are configured to communicate by default with the WeNet production instance.

To create a Wenet collector using an apikey as authorization you can use:

```python
from wenet.interface.client import ApikeyClient
from wenet.interface.wenet import WeNet


client = ApikeyClient("your_apikey")

wenet = WeNet.build(client)

# Using the wenet collector you can have access to all the interfaces methods, for example you can get all the tasks doing:
wenet.service_api.get_all_tasks()
```

To create a Wenet collector using an OAuth2 as authorization you can use:

```python
from wenet.interface.client import Oauth2Client
from wenet.interface.wenet import WeNet
from wenet.storage.cache import InMemoryCache


client = Oauth2Client.initialize_with_code(
    "client_id",
    "client_secret",
    "code",
    "redirect_url",
    "resource_id",
    InMemoryCache()
)

wenet = WeNet.build(client)

# Using the wenet collector you can have access to all the service apis methods, for example you can get all the tasks doing:
wenet.service_api.get_all_tasks()
```
