# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['sanic_jwt_extended']

package_data = \
{'': ['*']}

install_requires = \
['PyJWT>=1.6.4,<2.0.0', 'flatten-dict>=0.2.0,<0.3.0', 'sanic>=18.12.0']

extras_require = \
{':python_version >= "3.6.0" and python_version < "3.7.0"': ['dataclasses']}

setup_kwargs = {
    'name': 'sanic-jwt-extended',
    'version': '1.0.dev4',
    'description': 'Extended JWT integration with Sanic',
    'long_description': '<h1 align="center">🛡 Sanic-JWT-Extended 🛡</h1>\n\n<div align="center"> \n\n[![Downloads](https://pepy.tech/badge/sanic-jwt-extended)](https://pepy.tech/project/sanic-jwt-extended)\n![PyPI](https://img.shields.io/pypi/v/sanic-jwt-extended.svg)\n![PyPI - Python Version](https://img.shields.io/pypi/pyversions/sanic-jwt-extended.svg)\n![code style](https://img.shields.io/badge/code%20style-black-black.svg)\n[![Documentation Status](https://api.netlify.com/api/v1/badges/c2cf1ea1-bae1-448f-b52c-0dea6516446a/deploy-status)](https://sanic-jwt-extended.seonghyeon.dev)\n\n</div>\n\n> **☢️\xa0This is README of 1.0.dev version. [Click here](https://github.com/NovemberOscar/Sanic-JWT-Extended/tree/v0.4.4) to checkout current stable version(v0.4.4)**\n\n## 🚀 What is Sanic-JWT-Extended?\nSanic-JWT-Extended is an open source Sanic extension that provides JWT support (comply with RFC standard)\n\n## 💡 Why Sanic-JWT-Extended?\nSanic-JWT-Extended not only adds support for using JSON Web Tokens (JWT) to Sanic for protecting views,\nbut also many helpful (and **optional**) features  built in to make working with JSON Web Tokens\neasier. These include:\n\n* Support for adding public claims with [namespacing](https://auth0.com/docs/tokens/concepts/claims-namespacing)\n* Support for adding private claims\n* [Refresh tokens](https://auth0.com/blog/refresh-tokens-what-are-they-and-when-to-use-them/)\n* Token freshness and separate view decorators to only allow fresh tokens\n* Access control\n* blacklist support with some built-in blacklist\n* Provides Token object for easier jwt manifulation\n\n## ⚡️ Installation\n```shell script\n$ pip install sanic-jwt-extended --pre\n```\n```shell script\n$ poetry add sanic-jwt-extended --git https://github.com/NovemberOscar/Sanic-JWT-Extended.git\n```\n```shell script\n$ pipenv install sanic-jwt-extended --pre\n```\n\n## 📚 Documentation\n<a href="https://sanic-jwt-extended.seonghyeon.dev">\n<img src="https://i.imgur.com/eXRmcKO.png)](https://sanic-jwt-extended.seonghyeon.dev/" width="300" />\n</a>\n\n\n## 🛠 Developing Sanic-JWT-Extended\n\n### Prerequesties\n- [poetry](https://github.com/sdispater/poetry)\n\n### Installaion\n```shell script\n$ make env\n```\nthis will install dependencies with poetry. if poetry not found, will install poetry.\n\n### Development\n- `make format`: this will format your code with `isort` and `black`\n- `make check`: this will lint your code with `isort`, `black`, and `pylint`\n- `make clean`: this will remove temporary things.\n\n### Commit Convention\n```\n<{verb}>({scope}): {summary}\n```\n\n### Testing\n- **TBD**\n',
    'author': 'Seonghyeon Kim',
    'author_email': 'kim@seonghyeon.dev',
    'url': 'https://github.com/NovemberOscar/Sanic-JWT-Extended',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
