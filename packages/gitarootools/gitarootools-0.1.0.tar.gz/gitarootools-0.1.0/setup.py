# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['gitarootools',
 'gitarootools.audio',
 'gitarootools.cmdline',
 'gitarootools.miscutils']

package_data = \
{'': ['*']}

install_requires = \
['tomlkit>=0.5.8,<0.6.0']

extras_require = \
{':python_version >= "3.6" and python_version < "3.7"': ['importlib_resources>=1.0.2,<2.0.0']}

entry_points = \
{'console_scripts': ['gm-imcpack = gitarootools.cmdline.imcpack:main',
                     'gm-imcunpack = gitarootools.cmdline.imcunpack:main',
                     'gm-subsong2subimc = '
                     'gitarootools.cmdline.subsong2subimc:main',
                     'gm-subsong2wav = gitarootools.cmdline.subsong2wav:main',
                     'gm-subsongconv = gitarootools.cmdline.subsongconv:main']}

setup_kwargs = {
    'name': 'gitarootools',
    'version': '0.1.0',
    'description': 'command line tools to work with Gitaroo Man game data',
    'long_description': "# gitarootools — command line tools to work with Gitaroo Man game data\n \n*Gitaroo Man* is a rhythm action video game for PlayStation 2. This set of tools allows\nyou to work with data from the game, converting game files to more viewable formats. In\nsome cases, files converted this way can be edited, converted back to a game format, and\nreinserted into the game.\n\n## Installation\nThe easiest way to install `gitarootools` is to use `pip`:\n```bash\npip install gitarootools\n```\n\n## Usage\nSee each tool's help and usage by running\n```bash\ngm-<toolname> -h\n```\n\n## Included tools\n### Audio\n\n**`gm-imcpack`**: pack an IMC audio container from subsongs\n\n**`gm-imcunpack`**: unpack subsongs from an IMC audio container\n\n**`gm-subsongconv`**: convert a subsong to another format\n\n**`gm-subsong2[subimc|wav]`**: convert multiple subsongs to the specified format\n\n## Resources\n* [Gitaroo Pals](https://discord.gg/ed6P8Jt) Discord server for help and support\n* [Issue Tracker](https://github.com/boringhexi/gitarootools/issues)",
    'author': 'Iris Nakamura',
    'author_email': 'boringhexi@pm.me',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/boringhexi/gitarootools',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
