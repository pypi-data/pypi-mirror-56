# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['topyn', 'topyn.commands']

package_data = \
{'': ['*'], 'topyn': ['configs/*']}

install_requires = \
['black==19.10b0',
 'click>=7.0,<8.0',
 'flake8-bugbear>=19.8,<20.0',
 'flake8-comprehensions>=3.1,<4.0',
 'flake8-print>=3.1,<4.0',
 'flake8>=3.7,<4.0',
 'mypy>=0.740.0,<0.741.0']

entry_points = \
{'console_scripts': ['topyn = topyn:console.run']}

setup_kwargs = {
    'name': 'topyn',
    'version': '0.2.0',
    'description': 'TOPyN: Typed Opinionated PYthon Normalizer',
    'long_description': '# TOPyN: Typed Opinionated PYthon Normalizer\n\n## About\n<p align="center">\n    <img src="scooter.svg" alt="Scooter" width="300"/>*\n</p>\nPython is quite a flexible language, something that is not so good if you start working in mid level size projects and/or in teams.\nOver the time we have found a set of rules that makes working with Python in this context easier, and once you get you use to them you want to apply them to every small Python snippet that you write.\n\nThe problem is that these rules depend on a set of packages and config files, and every time we change our mind about one rule, or add new ones, we need to update multiple projects.\nTopyn solves this by providing in one single place all the tools and configurations we use in our projects.\n\nAll the configurations are part of the project (`topyn/configs`) and is not the purpose of this project to make them flexible, if you need that please check the packages that we use, and run them with your configuration.\n\n## Install\n`pip install topyn`\n\n## Command line\nThere are two possible arguments:\n* `path` is the path that you want to check, if it is empty it defaults to the current directory.\n* `--fix` if you use this flag topyn will try to fix the code for you\n\n### Examples\nCheck the code inside directory_with_code : `topyn directory_with_code`\n\nCheck the code inside current directory : `topyn`\n\nCheck the code inside current directory and try to fix it: `topyn --fix`\n\n### `topyn --help` output\n\n```\nTyped Opinionated PYthon Normalizer\n\npositional arguments:\n  path        path to topynize (default: .)\n\noptional arguments:\n  -h, --help  show this help message and exit\n  --fix       try to fix my code (default: False)\n  --version   show program\'s version number and exit\n```\n\n### `topyn` output\n✅\n```\n➡️ Checking formatting ...\nAll done! ✨ 🍰 ✨\n8 files would be left unchanged.\n➡️ Checking rules ...\n➡️ Checking types ...\n✅ Everything is OK! 😎"\n```\n🔴 \n```\n➡️ Checking formatting ...\nAll done! ✨ 🍰 ✨\n1 file would be left unchanged.\n➡️ Checking rules ...\n➡️ Checking types ...\ntests/resources/wrong_types/wrong_types.py:2: error: Incompatible return value type (got "int", expected "str")\nFound 1 error in 1 file (checked 1 source file)\n\n🔴 Sadly, types failed 😢\n```\n\n\n## Tools included\n\n### [Flake8](https://github.com/PyCQA/flake8)\nflake8 is a command-line utility for enforcing style consistency across Python projects\n\n#### Flake8 plugins\n* #### [flake8-bugbear](https://github.com/PyCQA/flake8-bugbear)\n  A plugin for flake8 finding likely bugs and design problems in your program. Contains warnings that don\'t belong in pyflakes and pycodestyle. \n* #### [flake8-print](https://github.com/JBKahn/flake8-print)\n  Check for `print` statements in python files.\n* #### [flake8-comprehensions](https://github.com/adamchainz/flake8-comprehensions)\n  A flake8 plugin that helps you write better list/set/dict comprehensions.\n### [Black](https://github.com/psf/black)\nThe Uncompromising Code Formatter\n### [Mypy](https://github.com/python/mypy)\nOptional static typing for Python (PEP 484) \n\n## Contributors\nLeandro Leites Barrios : Main developer\n\nDenada Korita : UX & Documentation consultant \n\n---\n\\* scooter icon source: [icons8](icons8.com)\n',
    'author': 'Leandro Leites Barrios',
    'author_email': 'laloleites@gmail.com',
    'url': 'https://github.com/lleites/topyn',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
