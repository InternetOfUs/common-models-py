# Wenet common models

<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->
**Table of Contents**

- [Models](#models)
- [Interface utilities](#interface-utilities)
- [Maintainers](#maintainers)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

This repository contains some common classes used in Wenet projects.


## Models
The repository contains the following models:
- users;
- tasks and transactions;
- norms;
- messages from the Wenet platform to the applications;
- App DTOs;
- messages for logging on Wenet


## Interface utilities
The repository also contains some utility classes to interface with the service API, and to handle exceptions.

For instantiating a collector of interfaces for an internal usage you can use `ServiceCollector.build()` specifying as environment variables:
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


## Maintainers

- Nicolò Pomini (nicolo.pomini@u-hopper.com)
- Carlo Caprini (carlo.caprini@u-hopper.com)
- Stefano Tavonatti (stefano.tavonatti@u-hopper.com)
