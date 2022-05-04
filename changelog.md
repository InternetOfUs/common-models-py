# Wenet common models - Changelog

## Version 1.0.4

- Fixed the task and profile models not using anymore the old norm model

## Version 1.0.3

- Added script for sending prompt message to users
- Updated Logger models
- Adjusted incentive badge and messages parser in order to align to unrequested breaking changes applied in the badge message content
- Minor fixes to WeNet models

## Version 1.0.2
- Bug fix on OAuth token refresh, in case the OAuth server returns a 400-coded response.

## Version 1.0.1
- Added models of messages to log requests, responses and notifications to the Wenet logging tool.
- Added support for redis caching system.

## Version 1.0.0
- First versions of the models of tasks, transactions, norms, users, messages for wenet apps and application DTOs;
- Utility functions to use the service API and to handle some exceptions.
