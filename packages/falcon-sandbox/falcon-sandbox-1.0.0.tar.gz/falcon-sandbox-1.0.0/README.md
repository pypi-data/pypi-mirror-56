# Falcon Sandbox python library

Python library for the [Falcon Sandbox API](https://www.falcon-sandbox.com/docs/api/v2) with command line wrapper. Library originally developed for use by [ACE](https://github.com/ace-ecosystem/ACE). The command line wrapper was written to more easily interact with a Falcon Sandbox for intel analysts and [Event Sentry](https://github.com/ace-ecosystem/eventsentry) consumption.

## Installation

``pip install falcon-sandbox``

## The falcon-sandbox CLI script

When installed, a command line script named 'falcon-sandbox' is supplied that can be used to interact with a Falcon Sandbox service.

The command line script looks for the configuration settings it needs at ``~/<current-user>/.config/falcon.ini``. The script will prompt you for the information it needs and write that file on the first execution if the file doesn't already exist. Like so:

```
$ falcon-sandbox get system -v
2019-11-22 16:46:38 analysis falcon_sandbox.helpers.load_config[8545] CRITICAL Didn't find any config files defined at these paths: ['/data/home/user/.config/falcon.ini']
Did not find user configuration, would you like to create one? [Y/n] 
FQDN of your Falcon sandbox server: private.falcon-sandbox.com
Your API key: oki53wxinm7ep8ja4ucomuyerfake5o9zi5bipvqvxskycrqxcfzqwkeea5ouvxg3
Do you need to use the system proxy to connect to the sandbox? [Y/n] 
2019-11-22 16:46:54 analysis root[8545] INFO Wrote user configuration to: /data/home/user/.config/falcon.ini
{'api': '2.6.0', 'instance': '8.6.1-0a10823e3', 'sandbox': '8.30'}
```

The root level help:
```
$ falcon-sandbox -h
usage: falcon-sandbox [-h] [-d] [--ignore-proxy] [--server-fqdn SERVER_FQDN]
                      [--api-key API_KEY] [--raw-json] [-w WRITE_OUTPUT]
                      [-t {xml,json,html,pdf,maec,stix,misp,misp-json,openioc}]
                      {search,submit,get} ...

A command line client for interacting with the Falcon Sandbox library written
for the ACE Ecosystem.

positional arguments:
  {search,submit,get}
    search              Search your Falcon sandbox
    submit              Submit a sample.
    get                 get info, artifacts, and results from the server.

optional arguments:
  -h, --help            show this help message and exit
  -d, --debug           set logging to DEBUG
  --ignore-proxy        ignore system proxy.
  --server-fqdn SERVER_FQDN
                        The fqdn of your Falcon sandbox server. Overrides
                        config.
  --api-key API_KEY     Pass an api key to use. Overrides any configured api
                        key.
  --raw-json            return the raw json results (don't pretty print)
  -w WRITE_OUTPUT, --write-output WRITE_OUTPUT
                        specify the name of a file to write results.
  -t {xml,json,html,pdf,maec,stix,misp,misp-json,openioc}, --report-type {xml,json,html,pdf,maec,stix,misp,misp-json,openioc}
                        The type of report you want. Default is json.
```

## Examples

### Submit

Submit files and URLS. The default behavior for the command line is to wait for the completion of jobs that are submitted and then download the entire result as json.

#### Files

For submissions from the command line the default behavior is to wait for the submission to complete and download all results as json.
Be aware the result files can be quite large. They are chunked on download for that reason.
```
$ falcon-sandbox submit -f PMNT_089_08102019.xls -e 100
2019-11-22 17:08:54 analysis falcon_sandbox[11412] INFO Got job id 5dd85bd85c757507273ee1dc for PMNT_089_08102019.xls submission
{'environment_id': 100,
 'job_id': '5dd85bd85c757507273ee1dc',
 'sha256': '6e5734c914eee85fcd56522857a00a10de76a6bb4fe533fd58d618acd21dfa1d',
 'submission_id': '5dd85bd85c757507273ee1db'}
2019-11-22 17:08:54 analysis falcon_sandbox[11412] INFO job 5dd85bd85c757507273ee1dc is in IN_QUEUE state..
2019-11-22 17:09:21 analysis falcon_sandbox[11412] INFO job 5dd85bd85c757507273ee1dc is in IN_PROGRESS state..
...
2019-11-22 17:15:03 analysis falcon_sandbox[11412] INFO job 5dd85bd85c757507273ee1dc is in IN_PROGRESS state..
2019-11-22 17:15:12 analysis falcon_sandbox[11412] INFO Job 5dd85bd85c757507273ee1dc has moved to a SUCCESS state
2019-11-22 17:15:12 analysis falcon_sandbox[11412] INFO Wrote 5dd85bd85c757507273ee1dc.falcon.json
```

#### URLs

```
$ falcon-sandbox submit -u 'https://firebasestorage.googleapis.com/v0/b/gu0-81b2b.appspot.com/o/index.html'
2019-11-22 17:16:48 analysis falcon_sandbox[12330] INFO Got job id 5dd85db23fec58f54c3ee1de for https://firebasestorage.googleapis.com/v0/b/gu0-81b2b.appspot.com/o/index.html submission
{'environment_id': 100,
 'job_id': '5dd85db23fec58f54c3ee1de',
 'sha256': '678895ccfd6c05d3f3bfba70fdea60a274181de66d94f356897d7d67875829a0',
 'submission_id': '5dd85db23fec58f54c3ee1dd',
 'submission_type': 'page_url'}
2019-11-22 17:16:48 analysis falcon_sandbox[12330] INFO job 5dd85db23fec58f54c3ee1de is in IN_QUEUE state..
2019-11-22 17:16:57 analysis falcon_sandbox[12330] INFO job 5dd85db23fec58f54c3ee1de is in IN_QUEUE state..
...
2019-11-22 17:23:33 analysis falcon_sandbox[12330] INFO job 5dd85db23fec58f54c3ee1de is in IN_PROGRESS state..
2019-11-22 17:23:40 analysis falcon_sandbox[12330] INFO Job 5dd85db23fec58f54c3ee1de has moved to a SUCCESS state
2019-11-22 17:23:41 analysis falcon_sandbox[12330] INFO Wrote 5dd85db23fec58f54c3ee1de.falcon.json
```

### Get

Get system info, analysis overviews, and all the various report data.

#### Get Overview Summary

```
$ falcon-sandbox get overview 6e5734c914eee85fcd56522857a00a10de76a6bb4fe533fd58d618acd21dfa1d -s
{'analysis_start_time': '2019-10-15T19:14:46+00:00',
 'last_multi_scan': '2019-11-22T21:37:49+00:00',
 'multiscan_result': None,
 'sha256': '6e5734c914eee85fcd56522857a00a10de76a6bb4fe533fd58d618acd21dfa1d',
 'threat_score': 55,
 'verdict': 'malicious'}
```

#### Get/Download the original sample.

```
$ falcon-sandbox get report 5da61a9d5c75754c1165dd98 -s
2019-11-22 17:00:53 analysis falcon_sandbox[10517] INFO Wrote PMNT_089_08102019.xls
```

#### Get the entire report as json

```
$ falcon-sandbox get report 5da61a9d5c75754c1165dd98 
2019-11-22 17:03:00 analysis falcon_sandbox[10760] INFO Wrote 5da61a9d5c75754c1165dd98.falcon.json
$
$ cat 5da61a9d5c75754c1165dd98.falcon.json | jq '.' | grep verdict -B 5 -A 5
        "threatsigimpact": "70",
        "theoreticalmaxthreatsigimpact": "5718",
        "theoreticalmaxthreatsigimpact_practical": "2802",
        "overallconfidence": "55"
      },
      "verdict": {
        "threatlevel": "2",
        "threatscore": "55",
        "isreliable": "true"
      },
      "signatures_triplets": "",
      "warnings": {
        "warning": [
          "Enforcing malicious verdict, as a reliable source indicates high confidence",
          "Not all sources for indicator ID \"api-55\" are available in the report"
        ]
      },
      "characteristics": {
        "has_carved_files": "false",
```

#### Get Available Environments

```
$ falcon-sandbox get system -e | grep description
  'description': 'Windows 7 32 bit',
  'description': 'Windows 7 64 bit',
  'description': 'Windows 10 64 bit',
  'description': 'Android Static Analysis',
  'description': 'Linux (Ubuntu 16.04, 64 bit)',
```

### Search

Search by hash(s), job_id(s), or terms.

#### Hashes

```
$ falcon-sandbox search -ha c1af0757c42aa3790719a6d5f64c57c5aa40af22916213758807eafe5e9e7351,8b764864c36daa127e3980c015839b5d5c0f5f7b482e2fe42a3a70808778b6af | grep job_id
  'job_id': '5dd6bd9f3fec583a48aeb00e',
  'job_id': '5dd66fc35c7575d80caeb00e',
```
#### Terms

Very basic searching by terms.
```
$ falcon-sandbox search -t 'filename:PMNT_089_08102019.xls'
{'count': 1,
 'result': [{'analysis_start_time': '2019-10-15 19:14:46',
             'av_detect': None,
             'environment_description': 'Windows 7 64 bit',
             'environment_id': 110,
             'job_id': '5da61a9d5c75754c1165dd98',
             'sha256': '6e5734c914eee85fcd56522857a00a10de76a6bb4fe533fd58d618acd21dfa1d',
             'size': 705024,
             'submit_name': 'PMNT_089_08102019.xls',
             'threat_score': 55,
             'type': None,
             'type_short': 'xls',
             'verdict': 'malicious',
             'vx_family': None}],
 'search_terms': [{'id': 'filename', 'value': 'PMNT_089_08102019.xls'}]}
 ```

 #### Job States

 ```
 $ falcon-sandbox search -s 5dd6bd9f3fec583a48aeb00e,5dd66fc35c7575d80caeb00e
[{'environment_id': 100,
  'error': None,
  'error_origin': None,
  'error_type': None,
  'job_id': '5dd6bd9f3fec583a48aeb00e',
  'query': '5dd6bd9f3fec583a48aeb00e',
  'related_reports': [],
  'sha256': 'c1af0757c42aa3790719a6d5f64c57c5aa40af22916213758807eafe5e9e7351',
  'state': 'SUCCESS'},
 {'environment_id': 100,
  'error': None,
  'error_origin': None,
  'error_type': None,
  'job_id': '5dd66fc35c7575d80caeb00e',
  'query': '5dd66fc35c7575d80caeb00e',
  'related_reports': [],
  'sha256': '8b764864c36daa127e3980c015839b5d5c0f5f7b482e2fe42a3a70808778b6af',
  'state': 'SUCCESS'}]
```
