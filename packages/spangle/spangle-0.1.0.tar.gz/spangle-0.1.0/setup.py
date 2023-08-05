# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['spangle', 'spangle.cli', 'spangle.models']

package_data = \
{'': ['*']}

install_requires = \
['addict>=2.2,<3.0',
 'aiofiles>=0.4.0,<0.5.0',
 'asgiref>=3.2,<4.0',
 'chardet>=3.0,<4.0',
 'httpx>=0.7.5,<0.8.0',
 'jinja2>=2.10,<3.0',
 'multidict>=4.5,<5.0',
 'multipart>=0.2.0,<0.3.0',
 'parse>=1.12,<2.0',
 'starlette>=0.12.12,<0.13.0']

entry_points = \
{'console_scripts': ['spangle = spangle.cli.run:main']}

setup_kwargs = {
    'name': 'spangle',
    'version': '0.1.0',
    'description': 'ASGI apprication framework inspired by `responder`, `vibora`, and `express-js`.',
    'long_description': '# spangle \n\nASGI apprication framework inspired by [responder](https://github.com/taoufik07/responder), [vibora](https://github.com/vibora-io/vibora), and [express-js](https://github.com/expressjs/express/). \n\n## Getting Started\n\n### Install\n\n```shell\npip install spangle\npip install hypercorn # or your favorite ASGI server\n```\n\n### Hello world\n\n```python\n# hello.py\nimport spangle\n\napi = spangle.Api()\n\n@api.route("/")\nclass Index:\n    async def on_request(self, req, resp):\n        resp.set_status(418).set_text("Hello world!")\n        return resp\n\n```\n\n```shell\nhypercorn hello:api\n```\n\n## Features\n\n* Component (from `vibora`!)\n* Flexible url params\n* `Jinja2` built-in support\n* Uniformed API\n* Single page apprication friendly\n\n...and more features. See [documents](http://tkamenoko.github.io/spangle).\n\n\n## Contribute\n\nContributions are welcome!\n\n* New features\n* Bug fix\n* Documents\n\n\n### Prerequisites\n\n* Python>=3.7\n* git\n* poetry\n* yarn\n\n### Build\n\n```shell\n# clone this repository.\ngit clone http://github.com/tkamenoko/spangle.git \n# install dependencies.\npoetry install\nyarn install\n```\n\n### Test\n\n```shell\nyarn test\n```\n\n### Update API docs\n\n```shell\nyarn doc:build\n```\n',
    'author': 'T.Kameyama',
    'author_email': 'tkamenoko@vivaldi.net',
    'url': 'https://github.com/tkamenoko/spangle',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7',
}


setup(**setup_kwargs)
