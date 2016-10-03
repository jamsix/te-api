#!/usr/bin/python

import urllib, urllib2
import json
import httplib
import time



class ThousandEyesApi:
    """
    ThousandEyesApi class provides methods to interact with the ThousandEyes API

    Attributes
    ----------
    email : str
        ThousandEyes platform user account

    authToken : str
        ThousandEyes platform user API token

    accountGroupId : str, optional
        ThousandEyes platform account group ID. If not set, user's default
        account group is used.

    Methods
    -------
    getRequest(endpoint, uriParameters = {})
        Performs GET HTTP request to desired API endpoint and returns JSON data
    postRequest(endpoint, parameters, uriParameters = {}):
        Performs POST HTTP request to desired API endpoint and returns JSON data
    """

    apiUri = 'https://api.thousandeyes.com'


    def __init__(self, email, authToken, accountGroupId=None):

        self.email = email
        self.authToken = authToken
        self.accountGroupId = accountGroupId


    def getRequest(self, endpoint, uriParameters = {}):
        """
        Performs GET HTTP request to desired API endpoint and returns JSON data

        Parameters
        ----------
        endpoint : str
            ThousandEyes API endpoint URL, such as '/agents'. Refer to
            http://developer.thousandeyes.com for the list of available endpoints.
        uriParameters : dict
            Dictionary of additional URL parameters, such as 'window'. Refer to the
            API endpoint documentation for the list of available parameters.

        Returns
        -------
        object
            ThousandEyes API result object. Refer to the API endpoint documentation
            for return object description.
        """

        """ Request JSON format in return """
        uriParameters['format'] = 'json'

        uri = self.apiUri.strip('/') + '/' + endpoint.strip('/') + '?' + urllib.urlencode(uriParameters)
        #print(uri)

        passwordManager = urllib2.HTTPPasswordMgrWithDefaultRealm()
        passwordManager.add_password(None, self.apiUri, self.email, self.authToken)
        handler = urllib2.HTTPBasicAuthHandler(passwordManager)

        director = urllib2.build_opener(handler)

        req = urllib2.Request(uri)

        """
        The ThousandEyes API throttles inbound API requests using a 240 request
        per minute, per organization limit.
        API request is encompassed with a for loop. If request returns a 429
        response code (Too many requests), it is repeated 10 seconds later, up
        to 10 times.
        """
        for n in range(0,10):
            try:
                """ Issue the API request """
                result = director.open(req)
            except urllib2.HTTPError, e:
                if 429 == e.code:
                    """ Issuing too many requests. Sleep 10 seconds and retry. """
                    time.sleep(10)
                    continue
                """ We cannot handle other HTTP errors """
                raise Exception("API HTTP error: " + str(e.code) + " " + str(e.reason))
            except urllib2.URLError, e:
                raise Exception("API URL error: " + str(e.reason))
            except httplib.HTTPException, e:
                raise Exception("API HTTP exception: " + str(e.reason))
            # result.read() will contain the data
            # result.info() will contain the HTTP headers

            return json.loads(result.read())

        return


    def postRequest(self, endpoint, properties, uriParameters = {}):
        """
        Performs POST HTTP request to desired API endpoint and returns JSON data

        Parameters
        ----------
        endpoint : str
            ThousandEyes API endpoint URL, such as '/agents'. Refer to
            http://developer.thousandeyes.com for the list of available endpoints.
        properties : dict
            ThousandEyes API endpoint properties that will be sent as POST payload.
            Refer to the API endpoint documentation for the list of available properties.
        uriParameters : dict
            Dictionary of additional URL parameters, such as 'window'. Refer to the
            API endpoint documentation for the list of available parameters.

        Returns
        -------
        object
            ThousandEyes API result object. Refer to the API endpoint documentation
            for return object description.
        """

        """ Request JSON format in return """
        uriParameters['format'] = 'json'

        uri = self.apiUri.strip('/') + '/' + endpoint.strip('/') + '?' + urllib.urlencode(uriParameters)
        #print(uri)

        passwordManager = urllib2.HTTPPasswordMgrWithDefaultRealm()
        passwordManager.add_password(None, self.apiUri, self.email, self.authToken)
        handler = urllib2.HTTPBasicAuthHandler(passwordManager)

        director = urllib2.build_opener(handler)

        headers = { 'Content-Type': 'application/json'}
        postData = json.dumps(properties)

        req = urllib2.Request(uri, postData, headers)

        """
        The ThousandEyes API throttles inbound API requests using a 240 request
        per minute, per organization limit.
        API request is encompassed with a for loop. If request returns a 429
        response code (Too many requests), it is repeated 10 seconds later, up
        to 10 times.
        """
        for n in range(0,10):
            try:
                """ Issue the API request """
                result = director.open(req)
            except urllib2.HTTPError, e:
                if 429 == e.code:
                    """ Issuing too many requests. Sleep 10 seconds and retry. """
                    time.sleep(10)
                    continue
                raise Exception("API HTTP error: " + str(e.code) + " " + str(e.reason))
            except urllib2.URLError, e:
                raise Exception("API URL error: " + str(e.reason))
            except httplib.HTTPException, e:
                raise Exception("API HTTP exception: " + str(e.reason))
            # result.read() will contain the data
            # result.info() will contain the HTTP headers

            return json.loads(result.read())

        return
