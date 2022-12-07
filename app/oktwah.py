#!/usr/bin/env python3

"""

This program is used to pull in Okta system logs and send them to Wazuh.  This will be accomplished 
by using the Okta API to pull in the logs and then send them to a log file where Wazuh will be able
pull them into the Wazuh server.

CODEOWNER: @mockingjay (mockingjay)
Org: MFG Consulting Concepts
Date: 2022-11-9
Version 0.0.1

Made with the help of our AI overlord, Copilot =).

"""

import os
import sys
import pathlib
import logging
import configparser
import argparse
import requests
import time
from datetime import datetime
from datetime import timedelta

# Define requried globals

parser = argparse.ArgumentParser(description='Okta Integration')
parser.add_argument('-c', '--conf', help='path to config file', default='/etc/okta/okta.conf')
args = parser.parse_args()

logging.basicConfig(filename='/var/log/okta/okta.log',
                    level=logging.INFO, format='%(asctime)s %(message)s',
                    datefmt='%m/%d/%Y %I:%M:%S %p')

config_file = args.conf
path = pathlib.Path(config_file)

if path.is_file():

    config = configparser.ConfigParser()
    config.read(args.conf)
    api = config['OktaTenant']['api']
    domain = config['OktaTenant']['domain']
else:
    logging.error(
        'Config file does not exist. Please create a config file. Template can be found at: '
        'https://github.com/Manufacturing-Consulting-Concepts/oktwah-py/blob/main/app/okta.conf')
    sys.exit(1)

# Functions

def current_time():
    nowtime = datetime.utcnow() - timedelta(minutes=5)
    ztime = nowtime.isoformat() + "Z"

    return ztime


# Test if Okta log files exists
def check_okta_log_exists():
    if os.path.isfile('/var/ossec/logs/okta/okta.log'):
        result = str("exists")
    else:
        os.mkdir('/var/ossec/logs/okta')
        open('/var/ossec/logs/okta/okta.log', 'x')
        result = str("created")
    return result


def check_program_log_exists():
    if os.path.isfile('/var/log/okta/okta.log'):
        result = str("exists")
    else:
        os.mkdir('/var/log/okta')
        open('touch /var/log/okta/okta.log', 'x')
        result = str("created")
    return result


# Get Okta Log Data
def create_session():
    s = requests.Session()
    s.headers.update({
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'Authorization': 'SSWS ' + api,
        'User-Agent': 'oktwah-py/0.2.* github.com/Manufacturing-Consulting-Concepts/oktwah-py'
    })

    def get_logs(r, *args, **kwargs):
        call_remaining = r.headers['x-rate-limit-remaining']
        if int(call_remaining) == 10:
            time.sleep(20)


    s.hooks['response'] = get_logs

    return s

def main():

    url = f"https://{domain}/api/v1/logs"
    params = {"sortOrder": "ASCENDING"}
    while True:
        sess = create_session()
        time.sleep(.7)
        response = sess.get(url, params=params)
        data = response


        url = data.links['next']['url']
        with open("/var/ossec/logs/okta/okta.log", "a+") as f:
            for line in data.json():
                f.write(str(line) + "\n")
        f.close()


if __name__ == "__main__":


    # Check if program log file exists
    application_log_file = check_program_log_exists()
    if application_log_file == "exists":
        pass
    else:
        logging.info('Okta log file did not exist. Created Okta log file.')

    # Check if Okta log file exists, and then log action
    okta_system_log_file = check_okta_log_exists()
    if okta_system_log_file == "exists":
        pass
    else:
        logging.info('Okta log file did not exist. Created Okta log file.')

    # Run main functions
    main()
