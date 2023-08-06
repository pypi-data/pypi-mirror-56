# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['json_pyformatter']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'json-pyformatter',
    'version': '0.1.0',
    'description': 'Python logging module outputs logs as JSON.',
    'long_description': '# json-pyformatter\n\n![GitHub Workflow Status](https://img.shields.io/github/workflow/status/homoluctus/json-pyformatter/Test)\n![GitHub release (latest by date including pre-releases)](https://img.shields.io/github/v/release/homoluctus/json-pyformatter?include_prereleases)\n![PyPI - Python Version](https://img.shields.io/pypi/pyversions/json-pyformatter)\n![GitHub](https://img.shields.io/github/license/homoluctus/json-pyformatter)\n\nPython logging outputs as JSON.<br>\nThis JsonFormatter is written in Pure Python.\n\n## Installation\n\n```bash\npip install json-pyformatter\n```\n\n## Usage\n\n```python\nimport logging\nfrom json_pyformmatter import JsonFormatter\n\nlogger = logging.getLogger(__name__)\nlogger.setLevel(logging.INFO)\nhandler = logging.StreamHandler()\nfields = (\'levelname\', \'filename\', \'message\')\nhandler.setFormatter(JsonFormatter(fields=fields))\nlogger.addHandler(hander)\n\nlogger.info(\'hello\')\n```\n\ndefault fields is (\'asctime\', \'levelname\', \'message\')<br>\nOther supported fields are:\n\n|field name|description|\n|:--:|:--|\n|name|Name of the logger (logging channel)|\n|levelno|Numeric logging level for the message<br>(DEBUG, INFO, WARNING, ERROR, CRITICAL)|\n|levelname|Text logging level for the message<br>("DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL")|\n|pathname|Full pathname of the source file where the logging call was issued|\n|filename|Filename portion of pathname|\n|module|Module (name portion of filename)|\n|lineno|Source line number where the logging call was issued|\n|funcName|Function name|\n|created|Time when the LogRecord was created (time.time()return value)|\n|asctime|Textual time when the LogRecord was created|\n|msecs|Millisecond portion of the creation time|\n|relativeCreated|Time in milliseconds when the LogRecord was created, relative to the time the logging module was loaded (typically at application startup time)|\n|thread|Thread ID|\n|threadName|Thread name|\n|process|Process ID|\n|message|The result of record.getMessage(), computed just as the record is emitted|\n\nIn details, please refere to [logrecord-attributes](https://docs.python.org/3/library/logging.html#logrecord-attributes)\n\n## Output\n\n```bash\n{"levelname": "INFO", "filename": "test_formatter.py", "message": "hello"}\n```\n\nIf specify indent option as 2, the result is as follows:\n\n```bash\n{\n  "levelname": "INFO",\n  "filename": "test_formatter.py",\n  "message": "hello"\n}\n```\n\nWhen exc_info is True, the result includes traceback infomation as follows:\n\n```bash\n{\n  \'asctime\': \'2019-12-01 13:58:34\',\n  \'levelname\': \'ERROR\',\n  \'message\': \'error occurred !!\',\n  \'traceback\': [\n    \'Traceback (most rec...ll last):\',\n    \'File "/example/test..._exc_info\',\n    \'raise TypeError(message)\',\n    \'TypeError: error occurred !!\'\n  ]\n}\n```\n\nLogging message type is dict:\n\n```bash\n{\n  \'asctime\': \'2019-12-01 23:34:32\',\n  \'levelname\': \'INFO\',\n  \'message\': {\n    \'id\': \'001\',\n    \'msg\': \'This is test.\',\n    \'name\': \'test\'\n  }\n}\n```\n',
    'author': 'homoluctus',
    'author_email': 'w.slife18sy@gmail.com',
    'url': 'https://github.com/homoluctus/json-pyformatter',
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
