#!/usr/bin/env python3

import os
import sys
import time
import json
import logging
import argparse
import coloredlogs
import pprint

from falcon_sandbox.helpers import load_config, create_user_config, parse_search_terms
from falcon_sandbox import FalconSandbox, VALID_SEARCH_TERMS, FS_REPORT_TYPES, FS_REPORT_TYPE_JSON, FS_STATUS_IN_QUEUE, FS_STATUS_IN_PROGRESS

# configure logging #
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - [%(levelname)s] %(message)s')

logger = logging.getLogger('falcon_sandbox')
coloredlogs.install(level='INFO', logger=logger)

def main():
    parser = argparse.ArgumentParser(description="A command line client for interacting with the Falcon Sandbox library written for the ACE Ecosystem.")
    parser.add_argument('-d', '--debug', action="store_true", help="set logging to DEBUG", default=False)
    parser.add_argument('--ignore-proxy', action='store_true', default=False, help='ignore system proxy.')
    parser.add_argument('--server-fqdn', action="store", help="The fqdn of your Falcon sandbox server. Overrides config.")
    parser.add_argument('--api-key', action='store',help="Pass an api key to use. Overrides any configured api key.")
    parser.add_argument('--raw-json', action="store_true", help="return the raw json results (don't pretty print)")
    parser.add_argument('-w', '--write-output', action='store', help="specify the name of a file to write results.")
    parser.add_argument('-t', '--report-type', action='store', choices=FS_REPORT_TYPES, default=FS_REPORT_TYPE_JSON, help="The type of report you want. Default is json.")

    subparsers = parser.add_subparsers(dest='instruction')

    parser_search = subparsers.add_parser('search', help="Search your Falcon sandbox")
    parser_search.add_argument('-ha', '--hashes', action='store', help="a comma separated list of hashes to search for")
    parser_search.add_argument('-s', '--states', action='store', help="comma separated list of job ids to get the state of.")
    parser_search.add_argument('-t', '--terms-query', action='store', help="comma separated list of terms to search for. Usage like -> term:value,term:value")
    parser_search.add_argument('--list-terms', action='store_true', help="List availbale search terms.")

    parser_submit = subparsers.add_parser('submit', help='Submit a sample.')
    parser_submit.add_argument('-f', '--file', action='store', help="file to submit.")
    parser_submit.add_argument('-u', '--url', action='store', help="url to submit.")
    parser_submit.add_argument('-e', '--environment_id', action='store', default='100', help='Enviroment to submit to. Default:100. Use "falcon_sandbox get system -e" to see availble environments.')
    parser_submit.add_argument('--arguments', action='store', default={}, help="Arguments to customize submission. Must be a dictionary.")
    parser_submit.add_argument('--hash-url', action='store', help="Get Falcon's custom sha256 hash for a URL.")
    parser_submit.add_argument('-r', '--reanalyze', action='store', help="The job_id of a sample to reanalyze.")

    parser_get = subparsers.add_parser('get', help='get info, artifacts, and results from the server.')
    parser_get.add_argument('-k', '--key-current', action='store_true', help='get current key info')
    parser_get_subs = parser_get.add_subparsers(dest='get_commands')

    parser_get_system = parser_get_subs.add_parser('system', help='get system info')
    parser_get_system.add_argument('-v', '--version', action='store_true', help='get the system version')
    parser_get_system.add_argument('-e', '--environments', action='store_true', help='get available environments')
    parser_get_system.add_argument('-s', '--stats', action='store_true', help='get system stats')
    parser_get_system.add_argument('-c', '--configuration', action='store_true', help='get system configuration')
    parser_get_system.add_argument('-qs', '--queue-size', action='store_true', help='get system queue size')
    parser_get_system.add_argument('-ts', '--total-submissions', action='store_true', help='get system total submissions')

    parser_get_overview = parser_get_subs.add_parser('overview', help='get analysis overview features')
    parser_get_overview.add_argument('sha256', help='the sha256 of the sample to work with')
    parser_get_overview.add_argument('-s', '--summary', action='store_true', help='overview summary')
    parser_get_overview.add_argument('-r', '--refresh', action='store_true', help='overview refresh')
    # not implementing because it's redundant and I'm in a hurry
    #parser_get_overview.add_argument('--download-sample', action='store_true', help='redundant with get report -s')

    parser_get_report = parser_get_subs.add_parser('report', help='get report info')
    parser_get_report.add_argument('job_id', help="the Falcon job id")
    parser_get_report.add_argument('-o', '--output-target-path', help="where to write the result file (default: {job_id}.falcon.{report-or-file_type})", default='{job_id}.falcon.{type}')
    parser_get_report.add_argument('-c', '--certificate', action='store', help='get report certificate by id')
    parser_get_report.add_argument('-s', '--sample', action='store_true', help="Download the sample file")
    parser_get_report.add_argument('-st', '--state', action='store_true', help="Get the job id report state")
    parser_get_report.add_argument('-sum', '--summary', action='store_true', help="Get the report summary")
    parser_get_report.add_argument('-ss', '--screen-shots', action='store_true', help="Get the report screen shots")
    parser_get_report.add_argument('-es', '--enhanced-summary', action='store_true', help="Get the report enhanced summary")
    parser_get_report.add_argument('-t', '--report-type', action='store', choices=FS_REPORT_TYPES, default=FS_REPORT_TYPE_JSON, help="The type of report you want. Default is json.")
    parser_get_report.add_argument('-m', '--memory-dumps', action='store_true', help="Get any available memory dumps for this job")
    parser_get_report.add_argument('-p', '--pcap', action='store_true', help="Get any available pcap for this job")
    parser_get_report.add_argument('-d', '--dropped_files', action='store_true', help="Get dropped files")
    parser_get_report.add_argument('-i', '--iocs', action='store', choices=['strict', 'broad'], help="Get report IOCs")

    args = parser.parse_args()

    config = load_config(required_options=['ignore_proxy', 'server', 'api_key'])
    if config is None:
        set_config = input("Did not find user configuration, would you like to create one? [Y/n] ") or 'Y'
        if set_config is 'Y' or set_config is 'y':
            server = input("FQDN of your Falcon sandbox server: ")
            api_key = input("Your API key: ")
            ignore_proxy = input("Do you need to use the system proxy to connect to the sandbox? [Y/n] ") or 'Y'
            ignore_proxy = True if ignore_proxy.upper() is 'Y' else False
            create_user_config(server, api_key, ignore_proxy)
            config = load_config(required_options=['ignore_proxy', 'server', 'api_key'])
        else:
            return

    if config.getboolean('ignore_proxy') or args.ignore_proxy:
        if 'https_proxy' in os.environ:
            del os.environ['https_proxy']
    
    server = args.server_fqdn if args.server_fqdn else config['server']
    api_key = args.api_key if args.api_key else config['api_key']

    falcon = FalconSandbox(api_key=api_key, hostname=server)

    # if we have a job_id after running the users commands the 
    # default behavior will be to wait for that job to complete
    # and write the results of the job to a local json file
    job_id = None

    if args.instruction == 'search':
        if args.list_terms:
            pprint.pprint(VALID_SEARCH_TERMS)
            return
        if args.hashes:
            hashes = args.hashes.split(',')
            if len(hashes) == 1:
                result = falcon.search_hash(hashes[0])
                result.raise_for_status()
                result = result.json()
                pprint.pprint(result) if not args.raw_json else print(result)
            else:
                result = falcon.search_hashes(hashes)
                result.raise_for_status()
                result = result.json()
                pprint.pprint(result) if not args.raw_json else print(result)
        if args.states:
            result = falcon.search_states(args.states.split(','))
            result.raise_for_status()
            result = result.json()
            pprint.pprint(result) if not args.raw_json else print(result)
        if args.terms_query:
            terms = parse_search_terms(args.terms_query)
            result = falcon.search_terms(**terms)
            result.raise_for_status()
            result = result.json()
            pprint.pprint(result) if not args.raw_json else print(result)

    if args.instruction == 'submit':
        if args.file:
            result = falcon.submit_file(args.file, args.environment_id, **args.arguments)
            result.raise_for_status()
            result = result.json()
            job_id = result['job_id']
            logger.info("Got job id {} for {} submission".format(job_id, args.file))
            pprint.pprint(result) if not args.raw_json else print(result)
        if args.url:
            result = falcon.submit_url(args.url, args.environment_id, **args.arguments)
            result.raise_for_status()
            result = result.json()
            job_id = result['job_id']
            logger.info("Got job id {} for {} submission".format(job_id, args.url))
            pprint.pprint(result) if not args.raw_json else print(result)
        if args.hash_url:
            result = falcon.submit_hash_for_url(args.hash_url)
            result.raise_for_status()
            result = result.json()
            pprint.pprint(result) if not args.raw_json else print(result)
        if args.reanalyze:
            result = falcon.submit_reanalyze(args.reanalyze)
            result.raise_for_status()
            result = result.json()
            pprint.pprint(result) if not args.raw_json else print(result)

    if args.instruction == 'get':
        if args.key_current:
            result = falcon.get_key_current()
            result.raise_for_status()
            result = result.json()
            pprint.pprint(result) if not args.raw_json else print(result)
        if args.get_commands == 'report':
            if args.report_type is FS_REPORT_TYPE_JSON: # check config if arg is default
                args.report_type = config['report_type'] if 'report_type' in config else args.report_type
            if args.output_target_path == '{job_id}.falcon.{type}':
                args.output_target_path = args.output_target_path.format(job_id=args.job_id, type='{type}')
            if args.sample:
                if '{type}' in args.output_target_path:
                    result = falcon.get_report_summary(args.job_id)
                    result.raise_for_status()
                    args.output_target_path = result.json()['submit_name']
                result = falcon.get_report_sample(args.job_id, target_path=args.output_target_path)
                result.raise_for_status()
                logger.info("Wrote {}".format(args.output_target_path))
            elif args.memory_dumps:
                args.output_target_path = args.output_target_path.format(type='memdump') if '{type}' in args.output_target_path else args.output_target_path
                result = falcon.get_report_memory_dumps(args.job_id, target_path=args.output_target_path)
                result.raise_for_status()
                logger.info("Wrote {}".format(args.output_target_path))
            elif args.pcap:
                args.output_target_path = args.output_target_path.format(type='pcap') if '{type}' in args.output_target_path else args.output_target_path
                result = falcon.get_report_pcap(args.job_id, target_path=args.output_target_path)
                result.raise_for_status()
                logger.info("Wrote {}".format(args.output_target_path))
            elif args.state:
                args.output_target_path = args.output_target_path.format(type='state') if '{type}' in args.output_target_path else args.output_target_path
                result = falcon.get_report_state(args.job_id)
                result.raise_for_status()
                result = result.json()
                pprint.pprint(result) if not args.raw_json else print(result)
            elif args.summary:
                args.output_target_path = args.output_target_path.format(type='sum') if '{type}' in args.output_target_path else args.output_target_path
                result = falcon.get_report_summary(args.job_id)
                result.raise_for_status()
                result = result.json()
                if args.write_output:
                    with open(args.write_output, 'w') as f:
                        f.write(json.dumps(result))
                    logger.info("Wrote {}".format(args.write_output))
                else:
                    pprint.pprint(result) if not args.raw_json else print(result)
            elif args.enhanced_summary:
                args.output_target_path = args.output_target_path.format(type='esum') if '{type}' in args.output_target_path else args.output_target_path
                result = falcon.get_report_enhanced_summary(args.job_id)
                result.raise_for_status()
                result = result.json()
                if args.write_output:
                    with open(args.write_output, 'w') as f:
                        f.write(json.dumps(result))
                    logger.info("Wrote {}".format(args.write_output))
                else:
                    pprint.pprint(result) if not args.raw_json else print(result)
            elif args.screen_shots:
                raise NotImplementedError()
            elif args.dropped_files:
                raise NotImplementedError()
            elif args.iocs:
                args.output_target_path = args.output_target_path.format(type='iocs.csv') if '{type}' in args.output_target_path else args.output_target_path
                result = falcon.get_report_iocs(args.job_id, args.iocs)
                result.raise_for_status()
                with open(args.output_target_path, 'w') as f:
                    f.write(result.text)
                logger.info("Wrote {}".format(args.output_target_path))
            else:
                args.output_target_path = args.output_target_path.format(type=args.report_type) if '{type}' in args.output_target_path else args.output_target_path
                result = falcon.get_report(args.job_id, _type=args.report_type, target_path=args.output_target_path, accept_encoding='gzip')
                result.raise_for_status()
                logger.info("Wrote {}".format(args.output_target_path))
        if args.get_commands == 'system':
            if args.version:
                result = falcon.get_system_version()
                result.raise_for_status()
                result = result.json()
                pprint.pprint(result) if not args.raw_json else print(result)
            if args.environments:
                result = falcon.get_system_environments()
                result.raise_for_status()
                result = result.json()
                pprint.pprint(result) if not args.raw_json else print(result)
            if args.stats:
                result = falcon.get_system_stats()
                result.raise_for_status()
                result = result.json()
                pprint.pprint(result) if not args.raw_json else print(result)
            if args.configuration:
                result = falcon.get_system_configuration()
                result.raise_for_status()
                result = result.json()
                pprint.pprint(result) if not args.raw_json else print(result)
            if args.queue_size:
                result = falcon.get_system_queue_size()
                result.raise_for_status()
                result = result.json()
                pprint.pprint(result) if not args.raw_json else print(result)
            if args.total_submissions:
                result = falcon.get_system_total_submissions()
                result.raise_for_status()
                result = result.json()
                pprint.pprint(result) if not args.raw_json else print(result)
        if args.get_commands == 'overview':
            if args.summary:
                result = falcon.overview_summary(args.sha256)
                result.raise_for_status()
                result = result.json()
                pprint.pprint(result) if not args.raw_json else print(result)
            elif args.refresh:
                result = falcon.overview_refresh(args.sha256)
                result.raise_for_status()
                result = result.json()
                pprint.pprint(result) if not args.raw_json else print(result)
            else:
                result = falcon.overview(args.sha256)
                result.raise_for_status()
                result = result.json()
                pprint.pprint(result) if not args.raw_json else print(result)

    if job_id is not None:
        result = falcon.get_report_state(job_id)
        result.raise_for_status()
        job_state = result.json()['state']
        initial_time = int(time.time())
        while job_state == FS_STATUS_IN_QUEUE or job_state == FS_STATUS_IN_PROGRESS:
            if (int(time.time()) - initial_time) % 10 == 0:
                initial_time+=9 # essentially, log again about every 9 seconds
                logger.info("job {} is in {} state..".format(job_id, job_state))
            result = falcon.get_report_state(job_id)
            result.raise_for_status()
            job_state = result.json()['state']
        logger.info("Job {} has moved to a {} state".format(job_id, job_state))
        output_filepath = args.write_output  if args.write_output else "{}.falcon.{}".format(job_id, args.report_type)
        result = falcon.get_report(job_id, _type=args.report_type, target_path=output_filepath, accept_encoding='gzip')
        result.raise_for_status()
        logger.info("Wrote {}".format(output_filepath))