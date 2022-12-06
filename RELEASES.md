# RELEASES

## Status Table

| Version | Status | Date | Stream |
|---------|--|------|--------|
| v0.0.1  | deprecated | 11-23-22 | alpha |
| v0.0.2  | deprecated | 11-23-22 | alpha |
| v0.1.0 | deprecated | 11-29-22 | beta | 
| v0.1.1 | deprecated | 11-30-22 | beta/patch |
| v0.1.2 | deprecated | 12-01-22 | beta/patch |
| v0.1.3 | maintained | 12-02-22 | beta/patch |

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