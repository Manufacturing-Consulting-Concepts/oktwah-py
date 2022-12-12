# RELEASES

## Status Table

| Version | Status | Date | Stream |
|---------|--|------|--------|
| v0.0.1  | deprecated | 11-23-22 | alpha |
| v0.0.2  | deprecated | 11-23-22 | alpha |
| v0.1.0 | deprecated | 11-29-22 | beta | 
| v0.1.1 | deprecated | 11-30-22 | beta/patch |
| v0.1.2 | deprecated | 12-06-22 | beta/patch |
| v0.1.3 | deprecated | 12-06-22 | beta/patch |
| v0.1.4 | deprecated | 12-06-22 | beta/patch |
| v0.2.0 | deprecated | 12-07-22 | beta |
| v0.2.1 | deprecated | 12-08-22 | beta/patch | 
| v0.2.2 | maintained | 12-12-22 | beta/patch | 


### v0.2.0

### Description

This is the official beta release two that introduces in major improvements and
Functionality.

### Features
1. "Log streaming" like functionality to give more realtime logs
2. API rate limiting prevention and handling to prevent 429 errors

### Changes
1. Removed self constructed URLs in query to Okta API.  Now uses pagination
   links provided by Okta API in response headers.
2. Removed now more bounded queries.  This is replaced with polling requests
3. Better session management to improved robustness and reliability.
4. Headers now contain the oktwah-py user agent

### Known Issues
1. The Okta API does not provide a way to get the total number of logs.  This
   means that the logs will be pulled until the API returns a 429 error.  This
   is not a problem for most use cases, but if you have a large number of logs
   in your Okta instance, you may want to consider using the "Log streaming"
   functionality. This possible issue is mitigated somewhat through our rate limiting prevention mechanisms
2. In the event of an application crash and a restart, duplicated logs may be pulled. We are working on a possible solutions
   The api does not keep track of the last log pulled, so we have to rely on the last time stamp of the last log pulled.
   This is not a perfect solution, but it is the best we can do at this time. We will be implementing this feature in beta 3

   
### v0.1.4

### Description

Patch for time query parmeters

### Features
1. NA

### Changes
1. Fixed error in conf file that was causing time parameters to fail
2. Fixed how time parameters are passed to the API via a new function
3. removed calls to `os.system()` to improve security
4. Changed position of while loop to improve performance
5. General code cleanup to improve readability

---
### v0.1.0

#### Description

First Beta release of oktwah-py

#### Features

1. Retrieve Okta System logs via API access
2. Built in Wazuh Decoders and rules for out-of-the-box alert generation
3. Timed retrieval every 5 minutes (No log streaming at this point.  Pull method used a "now minus 5 minuts" method)
4. Runs as daemon
5. Application logging for better debugging and trouble shooting.

#### Changes

1. Improved README for better understanding of application configuration and maintenance.
2. Fixed systemd file
3. Improved build.sh script now has rudimentary distro detection to configure application based off of unique distinctions


### v0.0.2

#### Description

Alpha release 2 of oktwah. Contains updated instructions for LPA read only admin user access.

#### Features

1. Improved instructions

#### Changes

1. greatly improved instructions in README.md

### v0.0.1

#### Description

Alpha release 1 of oktwah

#### Features

1. Pulls in logs for Okta for analysis in Wazuh

#### Changes

1. initial alpha release