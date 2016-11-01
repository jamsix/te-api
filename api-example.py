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
import calendar
import csv



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


    def getPureUrlRequest(self, uri):
        """
        Performs GET HTTP request to desired API URL and returns JSON data
        Does not manage parameters. Use for pagination

        Parameters
        ----------
        url : str
            ThousandEyes API endpoint URL

        Returns
        -------
        object
            ThousandEyes API result object. Refer to the API endpoint documentation
            for return object description.
        """

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





"""

 Showcase script that utilizes the ThousandEyesApi class. Modify to achieve
 your desired results.

"""

"""
 ThousandEyes API requires username and API token. These should be provided as
 parameters from the CLI. User can optionally provide a number of an example to
 be ran. Defaults to example #1.
"""
if len(sys.argv) < 3 and len(sys.argv) > 7:
    sys.exit('Use: ' + sys.argv[0] + ' <email> <apiToken> [exampleNumber]')

username = sys.argv[1]
apiToken = sys.argv[2]
if len(sys.argv) >= 4:
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
        print str(e)
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
        print str(e)
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



"""
    Example #3

    This example gets the dns test data for the test id and aggregates to calculate
    the availability for the given test across all servers and agents.
    NOTE: Only gets the data for the last round of testing!
    NOTE: If the test is still in progress, it will return partial data.
"""
if exampleNo == 3:
    if not len(sys.argv) == 5:
        sys.exit('Use: ' + sys.argv[0] + ' <email> <apiToken> <exampleNumber> <testId>')
    testId  = sys.argv[4]

    """ Establish the API object with credentials
        Get the test data for the testId. """
    api = ThousandEyesApi(username, apiToken)
    testData = api.getRequest('/dns/server/' + str(testId) + '.json')

    """ Check if we have a DNS test on our hands otherwise we exit """
    if not (testData['dns']['test']['type'] == 'dns-server'):
        sys.exit('This example requires a DNS server test.')

    """ Iterate the DNS results and analyze response. """
    numTest = 0
    numSuccessful = 0

    for server in testData['dns']['server']:
        numTest += 1
        """ If resolutionTime is present in test result that means the test was Successful. """
        if 'resolutionTime' in server:
            numSuccessful += 1
    availability = float(numSuccessful) / float(numTest)

    print 'Availability for the last test run is {0:.2f}%.'.format(100*availability)


"""
    Example #4
    In this example we take the DNS Trace test data in a time window (parameter)
    and aggregate the mappings per agent over time (in time periods - parameter)
    in a form of an CSV file which gets created in working directory.
    The test in question has to be configured to get only A records.
    Agents are specified in first column, then for each time period a column is created
    and all of the mappings are semicolon separated in the cell.

    Use case: Track potential changes to mappings over time from multiple locations
    to verify geo load balancing

    Parameters:
        Test ID:     DNS trace test ID.
        Time window: (Optional) Time window for which we generate the CSV file in days (Default 2)
        Time period: (Optional) Time period for mapping aggregation in hours (Default 1 hour).
    Output:
        Output*.csv file in working directory
"""

def loadTestData(api, testId):
    """ Get the test data from the API for the test ID and given parameters. """
    testData = api.getRequest('/dns/trace/' + str(testId) + '.json', uriParameters)

    """ Check if we have a DNS trace test on our hands otherwise we exit. """
    if not (testData['dns']['test']['type'] == 'dns-trace'):
        sys.exit('This example requires a DNS trace test.')
    """
    Check if really have an A record test on our hands otherwise we exit.
    The domain field specifies domain under test and record type.
    """
    if not (testData['dns']['test']['domain'][-2:] == ' A'):
        sys.exit('This example requires a DNS trace test for A record.')

    """ Build a list of all traces for the test in the time window. """
    traces = list()
    traces.extend(testData['dns']['trace'])

    """
    Now check if have multiple pages and add all of them to traces.
    If a "next" field is present in "pages" we have another page and the "next"
    field provides a full URL for it.
    """
    while 'next' in testData['pages'].keys():
        """ Show progress. """
        sys.stdout.write('.')
        sys.stdout.flush()
        """ Call the API again with next page URL provided in the response. """
        testData = api.getPureUrlRequest(testData['pages']['next'])
        traces.extend(testData['dns']['trace'])
    print '\n'
    return traces

def processTraces(traces):
    """ Create a data map which holds the aggregated trace data. """
    data = {}

    for trace in traces:

        """ Get the date from the trace date/time in epoch. """
        traceEpoch = calendar.timegm(time.strptime (trace['date'], '%Y-%m-%d %H:%M:%S'))

        """ Calculated time period ID. """
        timePeriodId = (traceEpoch - startWindowTimeEpoch) / timePeriodSec
        if timePeriodId == -1:
            """
            Because the API returns all the rounds that are within the window, we
            can possiblly get a round which is before our calculated window.
            In this case we get a -1 time period ID, which we add to the first
            period (timePeriodId = 0) for simplification.
            """
            timePeriodId = 0
        """
        Check if the agent is in the data map already and add an empty list
        for the key if not.
        """
        if trace['agentName'] not in data.keys():
            data[trace['agentName']] = {}
        """
        Check if the time period exists for the agent and add the current
        mapping into a map for the period. It's a simple way to avoid duplication
        of the mappings and avoid a flood of data if we specify larger time
        windows.
        """
        if timePeriodId not in data[trace['agentName']].keys():
            data[trace['agentName']][timePeriodId] = {}
        """ If a trace fails, we get an errorDetails field in the JSON. """
        if not 'errorDetails' in trace.keys():
            data[trace['agentName']][timePeriodId][trace['mappings']] = ''
        else:
            """ To make it clear there was an error lets put a key in the map. """
            data[trace['agentName']][timePeriodId]['ERROR'] = ''
    return data

def generateCSV(fName, data):
    """ Open the file """
    f = open(fName, 'wt')
    try:
        csvWriter = csv.writer(f)
        csvWriter.writerow(['Output'])
        """ Handle the labels for the columns and tag them with start time. """
        isFirstRow = True
        firstRow = ['']
        for agent in data:
            """ Build a row to be written. """
            row = []
            row.extend([agent])
            for period in data[agent]:
                """ Gather the start times for the periods and format. """
                if isFirstRow:
                    firstRow.extend([time.strftime('%x %X', time.gmtime(startWindowTimeEpoch + period * timePeriodSec))])

                """ For each period, go through all the mappings and add to row. """
                mapjoin=''
                for mapping in data[agent][period].keys():
                    """ Concat mappings and ; separate. """
                    mapjoin += mapping + ';'
                """ Remove the last ;. """
                mapjoin = mapjoin[:-1]
                row.extend([mapjoin])


            """ Handle the first row. """
            if isFirstRow:
                csvWriter.writerow(firstRow)
                isFirstRow = False
            """ Write the row. """
            csvWriter.writerow(row)
    finally:
        f.close()

if exampleNo == 4:

    """ Parse the input parameters. """
    if   len(sys.argv) < 5 or len(sys.argv) > 7 :
        sys.exit('Use: ' + sys.argv[0] + ' <email> <apiToken> <example number> <test ID> [time window] [time period]')
    testId  = sys.argv[4]
    if len(sys.argv) >= 6:
        timeWindow = sys.argv[5]
    else:
        timeWindow = '2'
    if len(sys.argv) == 7:
        timePeriod = int(sys.argv[6])
    else:
        timePeriod = 1


    """ Set the window parameter. """
    uriParameters = {}
    uriParameters['window'] = timeWindow + 'd'

    """ Establish the API object with credentials. """
    api = ThousandEyesApi(username, apiToken)

    """
    Define a start time and end time data set in epoch:
        endWindowTimeEpoch = current time
        startWindowTimeEpoch = current time - time window in secconds
    """
    endWindowTimeEpoch = calendar.timegm (time.gmtime ())
    timeWindowSec = int(timeWindow) * 24 * 60 * 60
    startWindowTimeEpoch = endWindowTimeEpoch - timeWindowSec
    timePeriodSec = timePeriod * 60 * 60

    traces = loadTestData(api, testId)

    """
    Go over the traces and split them into a new multi dimensional map where:
    -agentName defines the key for map of agents.
    -timeperiod defines the the key for a map containing list of mappings.
    -mappings list will contain all the mappings received by the agent in the
        traces that fall into a time period.

    Time period is calculated in the following way:
    (traceEpoch - startWindowTimeEpoch) / timeWindowSec
    """

    data = processTraces(traces)

    """
    This is where we build the output CSV file.
    Agents are listed in first column.
    Each time period for each agent has column as well.
    Each cell gets the mappings for a particular time period.

    Go over the agents and then for each agent/time period put the mappings
    into a row.
    """
    """ File name. """
    fName = 'output'+str(endWindowTimeEpoch)+'.csv'

    generateCSV(fName, data)

    print 'Completed!\nWrote out {}\n'.format(fName)
