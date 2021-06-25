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

For instantiating a collector of interfaces you can use `WeNet.build()`.
If you are an internal developer, you can pass to in an `ApikeyClient` and use all the interfaces.
If you are an external developer, you have to pass to it an `Oauth2Client` in order to authenticate your requests and can only use the service api interface.


## Maintainers

- Nicolò Pomini (nicolo.pomini@u-hopper.com)
- Carlo Caprini (carlo.caprini@u-hopper.com)
- Stefano Tavonatti (stefano.tavonatti@u-hopper.com)
