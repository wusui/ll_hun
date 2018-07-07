#!/usr/bin/python3
"""
Login to LL site:
    USER_INFO is an ini file that contains:
         [DEFAULT]
         username: <Your user name>
         password: <Your password>
         active_season: current (or next) LL season number
         verbose: yes or no:
"""
import requests
import configparser

HEAD = "https://learnedleague.com/"
USER_INFO = "userinfo.ini"

def get_session():
    """
    Read the user supplied ini file and get a requests session
    also pass back active season number read from ini file.
    """
    payload = {}
    config = configparser.ConfigParser()
    config.read(USER_INFO)
    payload['username'] = config['DEFAULT']['username']
    payload['password'] = config['DEFAULT']['password']
    payload['login'] = 'Login'
    s=requests.Session()
    s.post('%sucp.php?mode=login' % HEAD, data=payload)
    verbosity = config.getboolean('DEFAULT', 'verbose')
    return (s, config['DEFAULT']['active_season'], verbosity)
