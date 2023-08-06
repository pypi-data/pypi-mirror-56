# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['cvlog']

package_data = \
{'': ['*']}

install_requires = \
['opencv-python>=3.4,<4.0']

setup_kwargs = {
    'name': 'opencv-log',
    'version': '1.0.0',
    'description': 'OpenCV based visual logger for debugging,logging and testing image processing code',
    'long_description': '# opencv-log\n\n[![CircleCI](https://img.shields.io/circleci/build/github/navarasu/opencv-log)](https://circleci.com/gh/navarasu/opencv-log) [![Coverage Status](https://img.shields.io/coveralls/github/navarasu/opencv-log/master)](https://coveralls.io/github/navarasu/opencv-log?branch=master) [![Pip Version](https://img.shields.io/pypi/v/opencv-log)](https://pypi.org/project/opencv-log) [![MIT License](https://img.shields.io/pypi/l/opencv-log)](https://github.com/navarasu/opencv-log/blob/master/LICENSE)\n\nOpenCV based visual logger for debugging, logging and testing image processing code\n\n## Usage\n\n```python\nimport cvlog as log\n\n# Set default mode and level\n# If we dont set, then default mode is NONE \n# and the default level is ERROR\nlog.set_mode(log.Mode.LOG)\nlog.set_level(log.Level.TRACE)\n\n# image read using opencv\n\nimg = cv2.imread("sample.img")\n\n# log or show the image or do nothing based on\n# the current mode and current level\n\n\nlog.image(log.Level.INFO, img)\n\nlog.image(log.Level.ERROR, img)\n\nlog.image(log.Level.TRACE, img)\n\n```\n\n## Modes\n\n```python\nimport cvlog as log\nlog.set_mode(log.Mode.DEBUG)\n\n```\n\nSet mode using ENV variable\n\n```python\nos.environ[\'CVLOG_MODE\'] = "DEBUG"\n```\n\n### Mode.NONE (Default)\n\nThis is the default mode if we don\'t set mode.\n\nUsed in production. It neither creates HTML file nor shows an image.\n\n### Mode.LOG\n\nLogs the image to interactive HTML to analyze the issue offline.\n\n![image](https://user-images.githubusercontent.com/20145075/69906004-ba752f00-13e2-11ea-8714-2425202148e8.png)\n\n### Mode.DEBUG\n\nShows the image using `cv2.imshow` instead of logging to debug steps in the development. \n\nIt on move on to next log step on pressing any key and exit the code on pressing `ESC`\n\n![image](https://user-images.githubusercontent.com/20145075/69906116-581d2e00-13e4-11ea-8fbe-c1c5f778bb05.png)\n\n## Levels\n\n```python\nimport cvlog as log\nlog.set_level(log.Level.TRACE)\n```\n\nor\n\n```python\nos.environ[\'CVLOG_MODE\'] = "TRACE"\n```\n\n* **Level.ERROR** (Default) - *Log or Show only ERROR level*\n* **Level.INFO** - *Log or Show INFO and ERROR level*\n* **Level.TRACE** - *Log or Show TRACE, INFO and ERROR level steps*\n \nLevel valid for DEBUG and LOG mode',
    'author': 'Navarasu',
    'author_email': 'navarasu@outlook.com',
    'url': 'https://github.com/navarasu/opencv-log',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.4,<4.0',
}


setup(**setup_kwargs)
