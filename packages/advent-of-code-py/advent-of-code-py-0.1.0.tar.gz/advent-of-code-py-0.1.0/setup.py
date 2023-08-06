# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['advent_of_code_py']

package_data = \
{'': ['*']}

install_requires = \
['appdirs==1.4.3', 'click==7.0', 'python-dateutil==2.8.1', 'requests==2.22.0']

entry_points = \
{'console_scripts': ['advent-of-code-py = advent_of_code_py.cli:main']}

setup_kwargs = {
    'name': 'advent-of-code-py',
    'version': '0.1.0',
    'description': 'Advent of Code helper CLI and library',
    'long_description': '# Advent-of-code-py\n[Advent of Code][advent_of_code_link] helper CLI and library for python projects.\n\n**Note:**\nCurrently it is still in beta stage which may have lots of bug please report out bug if you find any\n\n**Status & Info:**\n\n| Travis Build Status | Code style | License |\n| :---: | :---: | :---: |\n| [![Travis Build Status][build_badge]][build_link] | [![Code style][black_badge]][black_link] | [![License: MIT][license_badge]][license_link] |\n\n## Usage\n\n### Installation\nTo install out advent-of-code-py run out following command which install out advent-of-code-py cli and advent_of_code_py library.\n```bash\npip install advent-of-code-py\n```\n\n__OR__\n\n```bash\npoetry add advent-of-code-py\n```\n\n### Usage\nInitially for advent-of-code-py to work out it need session value or session ID which you can obtain out by viewing out cookie while visiting advent of code server.\nAfter collecting session cookie value you need to add those value in config using advent-of-code-py CLI\n```bash\nadvent-of-code-py config add <session-name> <session-value>\n```\n\nNow you can import out library by using\n```python\nimport advent_of_code_py\n```\n\nAfter importing a library you can now use out either two decorator solve or submit decorator for a function of puzzle\n\nFor example:-\n```python\n@advent_of_code_py.submit(2018,3,1,session="<session-name>")\ndef puzzle_2018_3_1(input):\n    # do some calculation\n    return final_output\n```\n\nNow after decorating out function now you can call out function\n```python\npuzzle_2018_3_1()\n```\nAfter calling out function `final_output` value will be submitted out to Advent of Code server for 2018 year day 3\nproblem then returns out whether submitted answer was correct or not. If session value is not provided then\nsolution will be submitted to all session value set out.\n\nYou can also use out advent-of-code-py builtin Initializer and runner to create out appropriate CLI\ntool for problem so problem can be run easily\nTo set advent-of-code-py puzzle as CLI\n```python\n@advent_of_code_py.adventrunner()\ndef main_cli():\n    initializer = advent_of_code_py.Initializer()\n    initializer.add("<function_alias>"="<function>")\n    # for example to run above function you can write out\n    initializer.add("2018-3-1"=puzzle_2018_3_1)  \n    # add other function\n    return initializer\n```\nNow you can set out main_cli as entry points and it will create out CLI with appropriate name and function which was added.\nSo for example to run out function puzzle_2018_3_1() you have to run out command as `entry-point-name run 2018-3-1` which\nwill run appropriate function as well as submit as desired.\n\n[advent_of_code_link]: https://adventofcode.com\n\n[build_badge]: https://img.shields.io/travis/com/iamsauravsharma/advent-of-code-py.svg?logo=travis\n[build_link]: https://travis-ci.com/iamsauravsharma/advent-of-code-py\n\n[black_badge]: https://img.shields.io/badge/code%20style-black-000000.svg\n[black_link]: https://github.com/ambv/black\n\n[license_badge]: https://img.shields.io/github/license/iamsauravsharma/advent-of-code-py.svg\n[license_link]: LICENSE\n',
    'author': 'Saurav Sharma',
    'author_email': 'appdroiddeveloper@gmail.com',
    'url': 'https://github.com/iamsauravsharma/advent-of-code-py',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
