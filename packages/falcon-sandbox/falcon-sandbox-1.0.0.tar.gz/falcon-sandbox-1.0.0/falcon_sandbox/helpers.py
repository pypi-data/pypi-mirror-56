#!/usr/bin/env python3

import os
import logging
from configparser import ConfigParser
from falcon_sandbox import VALID_SEARCH_TERMS

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def load_config(profile='default', required_options=[]):
    """Load a Falcon sandbox configuration. Configuration files are user specific::
        ~/<current-user>/.config/falcon.ini
    :param str profile: (optional) Specifiy a group or company to work with.
    """
    logger = logging.getLogger(__name__+".load_config")
    config = ConfigParser()
    config_paths = []
    # user specific
    config_paths.append(os.path.join(os.path.expanduser("~"),'.config','falcon.ini'))
    finds = []
    for cp in config_paths:
        if os.path.exists(cp):
            logger.debug("Found config file at {}.".format(cp))
            finds.append(cp)
    if not finds:
        logger.critical("Didn't find any config files defined at these paths: {}".format(config_paths))
        return None

    config.read(finds)
    try:
        config[profile]
    except KeyError:
        logger.critical("No section named '{}' in configuration files : {}".format(profile, config_paths))
        return False

    for op in required_options:
        if not config.has_option(profile, op):
            logger.error("Configuation missing required options: {}".format(op))
            return False
        elif not config[profile][op]:
            logger.error("Configuration option missing value: {}".format(op))
            return False

    return config[profile]

def create_user_config(server, api_key, ignore_proxy):
    """Creates a minimal configuration for the user.
    """
    config = ConfigParser()
    # user specific
    config_path = os.path.join(os.path.expanduser("~"),'.config','falcon.ini')
    config['default'] = {'server': server,
                         'api_key': api_key,
                         'ignore_proxy': ignore_proxy}
    with open(config_path, 'w') as configfile:
        config.write(configfile)
    logging.info("Wrote user configuration to: {}".format(config_path))
    return

def parse_search_terms(query_str):
    """This function converts a string from field:value pairs into \*\*args that FalconSandbox.search_terms can recognize.
    :param str query_str: A query string to be parsed where the term:value are comma seperated.
    :return: \*\*args
    """
    ## SIMPLE implementation..
    logger = logging.getLogger(__name__+".parse_search_terms")
    query_parts = query_str.split(',')
    args = {}
    for part in query_parts:
        field = part[:part.find(':')]
        if field not in VALID_SEARCH_TERMS:
            logger.critical("{} is not a valid search term. Valid terms: {}".format(field, VALID_SEARCH_TERMS))
            return False
        value = part[part.find(':')+1:]
        args[field] = value
    return args