#!/usr/bin/python
import sys
import time
import calendar
import csv
from teapi import ThousandEyesApi

"""
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
    Check if results have an A record test on our hands otherwise we exit.
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
    """
        Processes the trace elements from the test results in the time
        window.
        Go over the traces and split them into a new multi dimensional map where:
        -agentName defines the key for map of agents.
        -timeperiod defines the the key for a map containing list of mappings.
        -mappings list will contain all the mappings received by the agent in the
            traces that fall into a time period.

        Time period is calculated in the following way:
        (traceEpoch - startWindowTimeEpoch) / timeWindowSec

        Parameters
        ----------
        traces : list
            List of trace elements from the API response

        Return
        -------
        data : map
            Map of DNS trace mappings split by agent and time period
    """
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

    """
        Build the output CSV file.
        Agents are listed in first column.
        Each time period for each agent has column as well.
        Each cell gets the mappings for a particular time period.

        Go over the agents and then for each agent/time period put the mappings
        into a row.

        Parameters
        ----------
        fName : String
            File name of CSV to be generated.
        data : map
            Map containing trace data to be written to the file

        Return
        ------
        null

    """

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

""" Parse the input parameters. """
if   len(sys.argv) < 4 or len(sys.argv) > 6 :
    sys.exit('Use: ' + sys.argv[0] + ' <email> <apiToken> <test ID> [time window] [time period]')

""" Set parameters """
username = sys.argv[1]
apiToken = sys.argv[2]
testId  = sys.argv[3]
if len(sys.argv) >= 5:
    timeWindow = sys.argv[4]
else:
    timeWindow = '2'
if len(sys.argv) == 6:
    timePeriod = int(sys.argv[5])
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

""" Get the data from the API and process it """
data = processTraces(loadTestData(api, testId))


""" Build unique file name. """
fName = 'output'+str(endWindowTimeEpoch)+'.csv'

""" Dump the the data into the CSV file """
generateCSV(fName, data)

print 'Completed!\nWrote out {}\n'.format(fName)
