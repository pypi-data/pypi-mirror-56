# dynamodb-traverse
High performance, thread safe, hackable, general purpose traversing tool for AWS DynamoDB based on aioboto3.
<p align="left">
<a href="https://travis-ci/holyshipt/dynamodb_traverse"><img alt="Build Status" src="https://travis-ci.org/holyshipt/dynamodb_traverse.svg?branch=master"></a>
<a href="https://pypi.org/project/dynamodb-traverse/"><img alt="Build Status" src="https://img.shields.io/pypi/v/dynamodb-traverse?color=green&label=latest"></a>
</p>

### Why manually traverse dynamodb table?
There're tens of ways to consume dynamodb data, for example, dynamodb stream, emr dynamodb connector, kinesis stream... they are good for different use cases. Manual traverse has following benefits comparing to these solutions:
* Deal with "small data"  
* Schema evolution, table migration 
* [Custom TTL mechanism](https://www.linkedin.com/pulse/top-reasons-why-you-should-implement-your-own-ttl-mechanism-he/)
* Full control over offline traversing
* Work with complicated nosql schema 
* Cross AWS account data replication/transformation

### Irrelevant use cases
Since `dynamodb-traverse` is not native to AWS, do not use if your use cases like:
* Real time streaming 
* Simple nosql schema that maps one primary key value to one sort key value
* Big data (~TB) workload that requires dedicated emr clusters
* Data backup

### Installation/Uninstallation
Prerequisite: python 3.8+ and aioboto3>=6.4.1 (bleeding edge)

Run following command to install requirements:

```shell script
$ pip install aioboto3
```

Next, install dynamodb-traverse by running:
```shell script
$ pip install dynamodb-traverse
```

To uninstall dynamodb-traverse, run:
```shell script
$ pip uninstall dynamodb-traverse
```

### Setup
* `dynamodb-traverse` by default looks at `~/.aws/credentials` for profiles you specified in the client. Make sure you have created profile to access dynamodb. 
* You can specify audit log location when initializing client. By default it writes to `/tmp/dynamodb_traverse_xxx.log`.
* We recommend using `35` as default scan batch size because of [dynamodb limitations](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/Limits.html)

### Usage

See `examples/traverse_source_table.py`

### create client
```
client = DynamoDBBase(
            queue=asyncio.Queue(loop=event_loop), 
            profile='string',
            log_file='string',
            local='boolean',
            **kwargs
         )
```

#### Parameters
* queue (Queue) [REQUIRED] - (async) in memory buffer queue 
    * event_loop (loop) [REQUIRED] - if use async queue, a loop need to be specified
* profile (string) [REQUIRED] - name of aws profile to use, which is defined in `.aws/credentials`
* local (boolean) [OPTIONAL] - a flag to indicate if it's local or prod env. Default to True.
* kwargs [OPTIONAL] - check [boto3](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb.html#client) for advanced usage

### traverse
```
 client.traverse(**{
       'producer': {
           'source': 'string',
           'TotalSegments': 'number',
           'Limit': 'number',
           'IndexName': 'string',
            **kwargs
        },
       'consumer': {
           'TotalSegments': 'number',
           'function': 'function_label',
           'timeout': 'number',
           'args': 'list',
        }
 })
```

#### Parameters
* producer (hash) [REQUIRED] - a hash describing the producer thread
    * source (string) [REQUIRED] - name of the source table in dynamodb
    * TotalSegments (number) [REQUIRED] - same in [boto3](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb.html#DynamoDB.Client.scan)
    * Limit (number) [REQUIRED] - same in [boto3](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb.html#DynamoDB.Client.scan)
    * IndexName (string) [OPTIONAL] - name of the source table index. If specified, we are scanning data from target index, instead of full table. 
    * kwargs (OPTIONAL) check [boto3](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb.html#DynamoDB.Client.scan) for more advanced usage.
    
* consumer (hash) [REQUIRED] - a hash describing the consumer thread
    * TotalSegments (number) - same in [boto3](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/dynamodb.html#DynamoDB.Client.scan)
    * function (function_label) - pass a function to this consumer!
    * args (list) - pass a list of args to the function you just supplied. currently we only support position based args
    * timeout (number) - how many second should consumer wait if there's no work load available to it immediately

### Benchmark (in progress)
