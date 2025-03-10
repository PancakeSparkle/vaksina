# Vaksina COVID QR Validation Checker

Vaksina is a general purpose library intended to validate multiple COVID QR codes from multiple countries and issuers. It is intended to streamline and help make validation of codes from multiple sources easier for public venues and other event.

This was primarilly written because, at the time I started this project, there is still no comprehensive COVID checking platform in existence. While some exist for Canada's SMART Health Cards, and the EU's Digital COVID Pass, there is no framework that can handle them as a single source of truth.

Vaksina is the intended proof of concept to handle this, and is intended to work with a REST based API deployed on venue, but may be adopted for use in mobile applications *and similar* as a future goal, but the intent is implementation with a kiosk like system that is used in combination with a national ID card *since* none of the COVID-19 QR codes are usable as an ID in and of themselves.

# Version 0.1 Goals

## Zero-Knowledge/Zero-Record Model

It is intended that no data submitted to Vaksina is stored beyond the time it takes to parse the record. The only external data loaded and kept are PKI information from a set of "known good" trusted sources, that is covered by the next bullet point.

## Creation of Public Trust Store

The creation of a "known good" set of sign keys will be provided ala Mozilla store.

## Creation of validation of SMART Health Card standard

There is no one specific standard for COVID-19 QR validation. Canada, and Japan have standardized on SMART, as have several states, pharmacies, hospitals and more within the United States. While Vaksina is intended as a general COVID-19 credential verification library, the initial MVP will only handle SMART Health Cards. Support for additional standards such as the EU's Digital COVID Pass, the UK's NHS Pass, and others like the New York State Excelsior Pass will be added with time.

## Implementation of VaccinePolicy Framework, to determine status

Given the ongoing needs of various venues, and other changes, it is planned that a given VaccinePolicy can coded for and changed. Vaksina is intended to have a "generic" frontend with current best practices, but is meant to be easily customized without having to fork the library.

## Basic Front End for testing purposes

For purposes of testing and validation, a simple REST frontend + javascript page for testing on a local install is intended as part of the MVP.

## Full code coverage and unit tests

Because we don't want to have untested code paths.
