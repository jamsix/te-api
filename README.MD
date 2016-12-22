

ThousandEyes API Examples
=========================

This library comprises of a few examples that were created for the usage of the
ThousandEyes API.

api-example.py
--------------
A basic ThousandEyes API script showcasing 3 Examples

1.  Print IP addresses of all Cloud Agents available to your account
2.  Create a new HTTP server test and add it to all Enterprise agents that are currently online.
3.  This example gets the dns test data for the test id and aggregates to calculate the availability for the given test across all servers and agents.

api-processDNSTrace.py
In this example we take the DNS Trace test data in a time window (parameter) and aggregate the mappings per agent over time (in time periods - parameter) in a form of an CSV file which gets created in working directory.
