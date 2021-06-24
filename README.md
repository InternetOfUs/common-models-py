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
from wenet.common.interface.collector import ServiceCollector

interface = ServiceCollector.build()
```

If necessary, it is possible to modify the urls of the target components by means of the following environment variables.

* `INSTANCE`: the instance to use, default is set to `https://internetofus.u-hopper.com/prod`;
* `APIKEY`: your apikey to be authorized to access the different components;
* `COMPONENT_AUTHORIZATION_APIKEY_HEADER`: the header for the component authorization via apikey, default is set to `x-wenet-component-apikey`;
* `HUB_PATH`: the path for the hub component, default is set to `/hub/frontend`;
* `INCENTIVE_SERVER_PATH`: the path for the incentive server component, default is set to `/incentive_server`;
* `LOGGER_PATH`: the path for the logger component, default is set to `/logger`;
* `PROFILE_MANAGER_PATH`: the path for the profile manager component, default is set to `/profile_manager`;
* `SERVICE_API_PATH_INTERNAL_USAGE`: the path for the hub component, default is set to `/service`;
* `TASK_MANAGER_PATH`: the path for the task manager component, default is set to `/task_manager`.

If you are an external developer, you can only use the service api component by instancing its interface `ServiceApiInterface`, you have to pass to it an `Oauth2Client` in order to authenticate your requests.
You can specify the path for the component using the following environment variable:
* `SERVICE_API_PATH_EXTERNAL_USAGE`:  default is set to `/api/service`.
