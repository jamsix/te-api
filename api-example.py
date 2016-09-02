#!/usr/bin/python

"""

 ThousandEyesApi class. Do not edit. Scroll down to the bottom to make changes

"""

import sys
import urllib, urllib2
import json
import datetime
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
                raise Exception("API HTTP error: " + str(e.code) + " " + e.reason)
            except urllib2.URLError, e:
                raise Exception("API URL error: " + e.reason)
            except httplib.HTTPException, e:
                raise Exception("API HTTP exception: " + e.reason)
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
                raise Exception("API HTTP error: " + str(e.code) + " " + e.reason)
            except urllib2.URLError, e:
                raise Exception("API URL error: " + e.reason)
            except httplib.HTTPException, e:
                raise Exception("API HTTP exception: " + e.reason)
            # result.read() will contain the data
            # result.info() will contain the HTTP headers

            return json.loads(result.read())

        return





"""

 Showcase script that utilizes the ThousandEyesApi class. Modify to achieve
 your desired results.

"""

"""
 ThousandEyes API requires username and API token. These should be provided as
 parameters from the CLI. User can optionally provide a number of an example to
 be ran. Defaults to example #1.
"""
if len(sys.argv) != 3 and len(sys.argv) != 4:
    sys.exit('Use: ' + sys.argv[0] + ' <email> <apiToken> [exampleNumber]')

username = sys.argv[1]
apiToken = sys.argv[2]
if len(sys.argv) == 4:
    exampleNo = int(sys.argv[3])
else:
    exampleNo = 1



"""
 Example #1

 Print IP addresses of all Cloud Agents available to your account
"""
if exampleNo == 1:

    """ Establish connection with the API, use your email and API token """
    api = ThousandEyesApi(username, apiToken)

    """ Get all agent data from the /agents API endpoint """
    try:
        data = api.getRequest('/agents')
    except Exception, e:
        print(e)
    else:
        """ Loop through all the agents """
        for agent in data['agents']:
            """ We are only interested in Cloud agents, not in Enterprise agents """
            if agent['agentType'] == 'Cloud':
                if agent['ipAddresses']:
                    """ Each Cloud agent has multiple IP addresses, loop through all """
                    for ipAddress in agent['ipAddresses']:
                        print(ipAddress)



"""
 Example #2

 Create a new HTTP server test and add it to all Enterprise agents that are
 currently Online.
"""
if exampleNo == 2:

    """ Establish connection with the API, use your email and API token """
    api = ThousandEyesApi(username, apiToken)

    """ Get all agent data from the /agents API endpoint """
    try:
        data = api.getRequest('/agents')
    except Exception, e:
        print(e)
    else:
        """ Put all Enterprise agent IDs in a single list """
        enterpriseAgentIds = []
        """ Loop through all the agents """
        for agent in data['agents']:
            """ We are only interested in Enterprise agents that are currently online """
            if agent['agentType'] == 'Enterprise' and agent['agentState'] == 'Online':
                enterpriseAgentIds.append(agent['agentId'])

        """ Test type is HTTP Server """
        testType = 'http-server'

        """
        Configure new test properties
        List of properties is found at http://developer.thousandeyes.com/tests/#/test_metadata
        """
        properties = {}
        """ Test will be called 'API test <date time>' """
        properties['testName'] = 'API test ' + datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S')
        """ Run once every hour """
        properties['interval'] = 3600
        """ Query the www.thousandeyes.com website """
        properties['url'] = 'http://www.thousandeyes.com'
        """ Disable alerts """
        properties['alertsEnabled'] = 0
        """ Run the test on the Enterprise agents that are currently online """
        properties['agents'] = []
        for agentId in enterpriseAgentIds:
            properties['agents'].append({"agentId": agentId})

        """ Create the test """
        result = api.postRequest('/tests/' + testType + '/new', properties)

        """ Print out the results of the new test call """
        print ('Test ' + result['test'][0]['testName'] + ' created.')
        print ('Currently running on agents:')
        for agent in result['test'][0]['agents']:
            print ('- ' + agent['agentName'])
