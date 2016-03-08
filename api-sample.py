#!/usr/bin/python

################################################################################
#
# ThousandEyesApi class. Do not edit. Scroll down to the bottom to make changes
#
################################################################################

import sys
import urllib2
import json

#
# ThousandEyesApi class includes methods to interact with the ThousandEyes API
#
class ThousandEyesApi:


    apiUri = 'https://api.thousandeyes.com/'


    def __init__(self, email, authToken, accountId=None):

        self.email = email
        self.authToken = authToken
        self.accountId = accountId


    def makeGetRequest(self, uri):

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


    def getAgents(self):

        uri = self.apiUri + 'agents.json'
        return self.makeGetRequest(uri)



################################################################################
#
# Showcase script that utilizes the ThousandEyesApi class. Modify to achieve
# your desired results.
#
################################################################################


if len(sys.argv) != 3 and len(sys.argv) != 4:
    sys.exit('Use: ' + sys.argv[0] + ' <email> <apiToken> [sampleNumber]')

# ThousandEyes API requires username and API token. These should be provided as
# parameters from the CLI.
username = sys.argv[1]
apiToken = sys.argv[2]
if len(sys.argv) == 4:
    sampleNo = int(sys.argv[3])
else:
    sampleNo = 1


#
# Sample #1
#
# Print IP addresses of all Cloud Agents available to your account
#
if sampleNo == 1:

    # Establish connection with the API, use your email and API token
    api = ThousandEyesApi(username, apiToken)

    # Get all agent data from the /agents API endpoint
    data = api.getAgents()

    # Loop through all the agents
    for agent in data['agents']:
        # We are only interested in Cloud agents, not in Enterprise agents
        if agent['agentType'] == 'Cloud':
            if agent['ipAddresses']:
                # Each Cloud agent has multiple IP addresses, loop through all
                for ipAddress in agent['ipAddresses']:
                    print(ipAddress)
