#!/usr/bin/python

"""

 ThousandEyesApi class. Do not edit. Scroll down to the bottom to make changes

"""

import sys
import urllib, urllib2
import json
from datetime import datetime, date
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
        ThousandEyes platform account group ID. If not set, user's default account group is used.

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

        try:
            result = director.open(req)
        except urllib2.HTTPError, e:
            print('HTTPError = ' + str(e.code))
        except urllib2.URLError, e:
            print('URLError = ' + str(e.reason))
        except httplib.HTTPException, e:
            print('HTTPException')
        # result.read() will contain the data
        # result.info() will contain the HTTP headers

        #response = requests.get(uri)
        return json.loads(result.read())


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

        try:
            result = director.open(req)
        except urllib2.HTTPError, e:
            print('HTTPError = ' + str(e.code))
        except urllib2.URLError, e:
            print('URLError = ' + str(e.reason))
        except httplib.HTTPException, e:
            print('HTTPException')

        return json.loads(result.read())





"""
 ThousandEyes API requires username and API token. These should be provided as
 parameters from the CLI. User can optionally provide a number of an example to
 be ran. Defaults to example #1.
"""
if len(sys.argv) != 3 and len(sys.argv) != 4:
    sys.exit('Use: ' + sys.argv[0] + ' <email> <apiToken> [reenable]')

username = sys.argv[1]
apiToken = sys.argv[2]
reenable = False
if len(sys.argv) == 4:
    reenable = sys.argv[3]
    if reenable.lower() == "true" or reenable == "1":
        reenable = True


issueStart = '2016-04-15 01:00:00'
issueEnd = '2016-04-15 02:00:00'

api = ThousandEyesApi(username, apiToken)

accData = api.getRequest('/accounts')

for account in accData['account']:

    aid = account['aid']

    data = api.getRequest('/tests', {'aid': aid})

    """ A list of enabled test IDs that were not modified since the T time """
    candidateTests = []

    for test in data['test']:
        if test['enabled'] == 1:
            if 'modifiedDate' in test.keys():
                dt = datetime.strptime(test['modifiedDate'], '%Y-%m-%d %H:%M:%S')
                if dt < datetime.strptime(issueStart, '%Y-%m-%d %H:%M:%S'):
                    candidateTests.append({'testId': test['testId'], 'type': test['type'], 'testName': test['testName']})

    """ A list of tests that need to be reenabled """
    reTests = []

    for test in candidateTests:
        time.sleep(0.1)
        results = []
        if test['type'] == 'http-server':
            data = api.getRequest('/web/http-server/' + str(test['testId']), {'aid': aid})
            results = data['web']['httpServer']
        elif test['type'] == 'page-load':
            data = api.getRequest('/web/page-load/' + str(test['testId']), {'aid': aid})
            results = data['web']['pageLoad']
        elif test['type'] == 'transaction':
            data = api.getRequest('/web/transactions/' + str(test['testId']), {'aid': aid})
            results = data['web']['transaction']
        elif test['type'] == 'dns-trace':
            data = api.getRequest('/dns/trace/' + str(test['testId']), {'aid': aid})
            results = data['dns']['trace']
        else:
            continue

        latestDate = datetime.strptime(issueEnd, '%Y-%m-%d %H:%M:%S')
        for result in results:
            if datetime.strptime(result['date'], '%Y-%m-%d %H:%M:%S') > latestDate:
                latestDate = datetime.strptime(result['date'], '%Y-%m-%d %H:%M:%S');

        if latestDate >= datetime.strptime(issueStart, '%Y-%m-%d %H:%M:%S') and latestDate <= datetime.strptime(issueEnd, '%Y-%m-%d %H:%M:%S'):
            reTests.append(test)
            print(str(test['testId']) + '\t' + account['accountName'] + '\t' + test['testName'])

    print(str(len(reTests)) + ' of ' + str(len(candidateTests)) + ' candidate tests have last result between ' + issueStart + ' and ' + issueEnd + ' UTC.')

    if (reenable == False):
        print ('Doing nothing about it. Set reenable argument to true to re-enable the probematic tests.')
    else:
        totalRe = 0;
        for test in reTests:
            time.sleep(0.2)
            print(test['testId'])
            result = api.postRequest('/tests/' + test['type'] + '/' + str(test['testId']) + '/update', {"enabled": 0}, {'aid': aid})
            print(result)
            result = api.postRequest('/tests/' + test['type'] + '/' + str(test['testId']) + '/update', {"enabled": 1}, {'aid': aid})
            print(result)
            sys.stdout.write('!')
            totalRe += 1

        print(str(totalRe) + ' tests re-enabled.')
