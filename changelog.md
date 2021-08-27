# Wenet common models - Changelog

## Version 2.*

### NEXT

* Included optional time filters for getting the users of an app in the hub interface
* Fixed put request of the outh2 client

### 2.0.0

* Re-organised project structure
* Re-organised all existing component interfaces: they are now based on the same base structure.
* Interfaces now support token-based and OAuth2 authentication strategies.
* Added new interfaces for allowing the communication with components in the platform. In particular, the Incentive Server, the Logging component and the Task Manager.
* Added script for removing those profiles that are not associated to any existing user.

## Version 1.*

### 1.1.0

- Added script for sending prompt message to users
- Updated Logger models
- Added TaskTransactionPage model
- Minor fixes to WeNet models

### 1.0.2
- Bug fix on OAuth token refresh, in case the OAuth server returns a 400-coded response.

### 1.0.1
- Added models of messages to log requests, responses and notifications to the Wenet logging tool.
- Added support for redis caching system.

### 1.0.0

- First versions of the models of tasks, transactions, norms, users, messages for wenet apps and application DTOs;
- Utility functions to use the service API and to handle some exceptions.
