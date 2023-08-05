# hns_console_logging
Just a simple script to create a logger object for logging to console. It is intended to be used with services running 
as docker container. By using the logging facility in docker container, you don't need to write logs to the file, you 
can use the logs written to file by docker daemon.  

## Installation
`pip install hns-console-logging`

## Usage
```python
import hns_console_logging
logger = hns_console_logging.get_logger('test_module')
logger.info('Info msg')
```
You can change the default log format and log level.  
Default log format: `%(asctime)s %(name)s %(funcName)s[PID:%(process)d TID:%(thread)d] %(levelname)s %(message)s`  
Default log level: `INFO`  

To change log format, please refer: https://docs.python.org/3/library/logging.html#logrecord-attributes  

