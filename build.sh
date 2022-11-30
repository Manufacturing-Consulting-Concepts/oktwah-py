#!/bin/bash

## Check if the user has root privileges
if [[ $UID -ne 0 ]]; then
    echo "This script needs to be run as root" 1>&2
    exit 1
fi

## check what distrobution of linux is being run. Supported versions are CentOS, debian, Ubuntu, Amazon Linux
if [ -f /etc/redhat-release ]; then
    OS="CentOS"
elif [ -f /etc/debian_version ]; then
    OS="Debian"
elif [ -f /etc/lsb-release ]; then
    OS="Ubuntu"
elif [ -f /etc/system-release ]; then
    OS="Amazon Linux"
else
    echo "This script is not supported on this OS"
    exit 1
fi

echo "detected OS is $OS"
echo " "

echo "setting up users and groups for oktwah"
    ## Setup oktwah service user
    useradd -m -s /bin/bash oktwah
    usermod -aG wazuh oktwah
echo " "

## If debian based distro is detected
if [ "$OS" == "Debian" ] || [ "$OS" == "Ubuntu" ]; then
    apt-get update -y 
    apt install python3 python3-pip git vim python3-venv -y
    cp assets/systemd/oktwah.service /etc/systemd/system/
    systemctl daemon-reload
    systemctl enable oktwah.service
    mkdir /etc/okta/ /var/log/okta/ /opt/oktwah/
    touch /var/log/okta/okta.log
    cp -r app/ /opt/oktwah
    chmod 755 /opt/oktwah/app/oktwah.py
    chown -R oktwah:wazuh /opt/oktwah/
    chmod 644 /etc/systemd/system/oktwah.service
    chown -R oktwah:wazuh /etc/okta/ /var/log/okta/ /opt/oktwah/ /var/log/okta/okta.log /var/ossec/logs/okta/

## If rhel based distro is detected
elif [ "$OS" == "CentOS" ] || [ "$OS" == "Amazon Linux" ]; then
    yum install python3 python3-pip git vim -y
    cp assets/systemd/oktwah.service /etc/systemd/system/
    systemctl daemon-reload
    systemctl enable oktwah.service
    mkdir /etc/okta/ /var/log/okta/ /opt/oktwah/ /var/ossec/logs/okta/
    touch /var/log/okta/okta.log
    cp -r app/ /opt/oktwah
    chmod 755 /opt/oktwah/app/oktwah.py
    chown -R oktwah:wazuh /opt/oktwah/
    chmod 644 /etc/systemd/system/oktwah.service
    chown -R oktwah:wazuh /etc/okta/ /var/log/okta/ /opt/oktwah/ /var/log/okta/okta.log /var/ossec/logs/okta/okta.log
fi


## copy the files to the correct locations
cp -r app /opt/oktwah/
cp requirements.txt /opt/oktwah/app/

## Configure Python3 env
python3 -m venv /opt/oktwah/app/env
source /opt/oktwah/app/env/bin/activate
pip3 install --upgrade pip
pip3 install -r /opt/oktwah/app/requirements.txt

## Copy rules and decoders to proper directories
cp wazuh/200500-okta_rule.xml /var/ossec/ruleset/rules/
cp wazuh/200500-okta_decoder.xml /var/ossec/ruleset/decoders/

## Restart Wazuh-manager
systemctl restart wazuh-manager