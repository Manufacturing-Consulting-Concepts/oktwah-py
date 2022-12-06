#!/usr/bin/env python3

"""

This program is used to pull in Okta system logs and send them to Wazuh.  This will be accomplished 
by using the Okta API to pull in the logs and then send them to a log file where Wazuh will be able
pull them into the Wazuh server.  This program will be run as a cron job every 5 minutes.

CODEOWNER: @mockingjay (mockingjay)
Org: MFG Consulting Concepts
Date: 2022-11-9
Version 0.0.1

Made with the help of our AI overlord, Copilot =).

"""

import os
import pathlib
import json
import logging
import configparser
import argparse
import requests
import time
from datetime import datetime
from datetime import timedelta


def current_time():
    nowtime = datetime.utcnow() - timedelta(minutes=5)
    ztime = nowtime.strftime("%Y-%m-%dT%H:%M:%S.000Z")

    return ztime

## Test if Okta log files exists
def check_okta_log_exists():
    if os.path.isfile('/var/ossec/logs/okta/okta.log'):
        result = str("exists")
    else:
        os.system('mkdir -p /var/ossec/logs/okta')
        os.system('touch /var/ossec/logs/okta/okta.log')
        result = str("created")
    return result


def check_program_log_exists():
    if os.path.isfile('/var/log/okta/okta.log'):
        result = str("exists")
    else:
        os.system('mkdir -p /var/log/okta')
        os.system('touch /var/log/okta/okta.log')
        result = str("created")
    return result


## Get Okta Log Data
def get_okta_log_data(api, url):
    # Get Okta log data using requests package
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'Authorization': 'SSWS ' + api
    }
    response = requests.get(url + ztime, headers=headers, timeout=10)
    data = response.json()

    return data


if __name__ == "__main__":

    while True:
        # initialize argsparser
        parser = argparse.ArgumentParser(description='Okta Integration')
        parser.add_argument('-c', '--conf', help='path to config file', default='/etc/okta/okta.conf')
        args = parser.parse_args()

        config_file = args.conf
        path = pathlib.Path(config_file)

        #################
        # Initial Setup #
        #################

        # Initialize loggingo
        logging.basicConfig(filename='/var/log/okta/okta.log',
                            level=logging.INFO, format='%(asctime)s %(message)s',
                            datefmt='%m/%d/%Y %I:%M:%S %p')

        # Check if Config file exists
        if path.is_file():
            # Read Config file
            config = configparser.ConfigParser()
            config.read(args.conf)
            api = config['OktaTenant']['api']
            url = config['OktaTenant']['url']
        else:
            logging.error(
                'Config file does not exist. Please create a config file. Template can be found at: https://someurl.com')
            exit()

        # Check if program log file exists, and then log action
        programLogFileResult = check_program_log_exists()
        if programLogFileResult == "exists":
            pass
        else:
            logging.info('Okta log file did not exist. Created Okta log file.')

        # Check if Okta log file exists, and then log action
        oktaLogFileResult = check_okta_log_exists()
        if oktaLogFileResult == "exists":
            pass
        else:
            logging.info('Okta log file did not exist. Created Okta log file.')

        #################
        # Get Okta Logs #
        #################

        # log okta pull start
        logging.info('Okta log pull started.')

        # Get Okta logs
        try:
            okta_log_data = get_okta_log_data(api, url)
            logging.info('Okta pull successful.')
        except Exception as e:
            logging.error('Okta log pull failed.  Error: {}'.format(e))

        # parse logs data and dump as json to okta log file
        try:
            with open('/var/ossec/logs/okta/okta.log', 'a+') as outfile:
                # Write one json object per line
                for entry in okta_log_data:
                    print(json.dumps(entry), file=outfile)
                outfile.close()
            logging.info('Okta log data dumped to file.')
        except Exception as e:
            logging.error('Okta log file write failed.  Error: {}'.format(e))

        time.sleep(300)
