# Wenet common models - Changelog

## NEXT

- Added script for analyzing users and profiles and spot misalignments
- Added clients for authentication in the interfaces
- Uniformed interfaces and added missing ones
- Aligned task manager and service api interfaces with the current documentation

## Version 1.1.0

- Added script for sending prompt message to users
- Updated Logger models
- Added TaskTransactionPage model
- Minor fixes to WeNet models

## Version 1.0.2
- Bug fix on OAuth token refresh, in case the OAuth server returns a 400-coded response.

## Version 1.0.1
- Added models of messages to log requests, responses and notifications to the Wenet logging tool.
- Added support for redis caching system.

## Version 1.0.0
- First versions of the models of tasks, transactions, norms, users, messages for wenet apps and application DTOs;
- Utility functions to use the service API and to handle some exceptions.
