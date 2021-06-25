# WeNet - Common models Library

This repository contains some common classes used in Wenet projects.


## Models

The library defines models that describe:

- users
- tasks and transactions
- norms
- messages from the WeNet platform to the applications
- app DTOs
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

```python
from wenet.interface.client import ApikeyClient
from wenet.interface.wenet import WeNet

interface = WeNet.build(ApikeyClient("your_apikey"))
```

If you are an internal developer, you can pass to in an `ApikeyClient` and use all the interfaces.
If you are an external developer, you have to pass to it an `Oauth2Client` in order to authenticate your requests and can only use the service api interface.
