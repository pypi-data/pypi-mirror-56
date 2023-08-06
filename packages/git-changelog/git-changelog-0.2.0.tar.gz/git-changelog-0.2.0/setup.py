# -*- coding: utf-8 -*-
from distutils.core import setup

package_dir = \
{'': 'src'}

packages = \
['git_changelog', 'git_changelog.templates']

package_data = \
{'': ['*'], 'git_changelog.templates': ['angular/*', 'keepachangelog/*']}

install_requires = \
['Jinja2>=2.10,<3.0']

entry_points = \
{'console_scripts': ['git-changelog = git_changelog.cli:main']}

setup_kwargs = {
    'name': 'git-changelog',
    'version': '0.2.0',
    'description': 'Automatic Changelog generator using Jinja2 templates.',
    'long_description': '<!--\nIMPORTANT: This file is generated from the template at \'scripts/templates/README.md\'.\n           Please update the template instead of this file.\n-->\n\n# git-changelog\n\n[![pipeline status](https://gitlab.com/pawamoy/git-changelog/badges/master/pipeline.svg)](https://gitlab.com/pawamoy/git-changelog/commits/master)\n[![coverage report](https://gitlab.com/pawamoy/git-changelog/badges/master/coverage.svg)](https://gitlab.com/pawamoy/git-changelog/commits/master)\n[![documentation](https://img.shields.io/readthedocs/git-changelog.svg?style=flat)](https://git-changelog.readthedocs.io/en/latest/index.html)\n[![pypi version](https://img.shields.io/pypi/v/git-changelog.svg)](https://pypi.org/project/git-changelog/)\n[![Gitter](https://badges.gitter.im/git-changelog/community.svg)](https://gitter.im/git-changelog/community?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge)\n\nAutomatic changelog generator. From git logs to change logs.\n\n**Table of contents**\n- [Features](#features)\n- [Requirements](#requirements)\n- [Installation](#installation)\n- [Usage as a library](#usage-as-a-library)\n- [Usage on the command line](#usage-command-line)\n- [Troubleshoot](#troubleshoot)\n\n## Features\n- [Jinja2][jinja2] templates!\n  You get full control over the rendering.\n  Built-in [Keep a Changelog][keep-a-changelog] and [Angular][angular] templates\n  (also see [Conventional Changelog][conventional-changelog]).\n- Commit styles/conventions parsing.\n  Built-in [Angular][angular-style], [Atom][atom-style] and basic styles.\n- Git service/provider agnostic,\n  plus references parsing (issues, commits, etc.).\n  Built-in [GitHub][github-refs] and [Gitlab][gitlab-refs] support.\n- Understands [Semantic Versioning][semantic-versioning]:\n  major/minor/patch for versions and commits.\n  Guesses next version based on last commits.\n\n- Todo:\n  - [Plugin architecture][issue-7],\n    to support more commit styles and git services.\n  - [Template context injection][issue-4],\n    to furthermore customize how your changelog will be rendered.\n  - [Easy access to "Breaking Changes"][issue-1] in the templates.\n  - [Update changelog in-place][issue-2], paired with\n    [commits/dates/versions range limitation ability][issue-3].\n\n[jinja2]:                 http://jinja.pocoo.org/\n[keep-a-changelog]:       http://keepachangelog.com/en/1.0.0/\n[angular]:                https://github.com/angular/angular/blob/master/CHANGELOG.md\n[conventional-changelog]: https://github.com/conventional-changelog/conventional-changelog\n[semantic-versioning]:    http://semver.org/spec/v2.0.0.html\n[atom-style]:             https://github.com/atom/atom/blob/master/CONTRIBUTING.md#git-commit-messages\n[angular-style]:          https://github.com/angular/angular/blob/master/CONTRIBUTING.md#commit\n[github-refs]:            https://help.github.com/articles/autolinked-references-and-urls/\n[gitlab-refs]:            https://docs.gitlab.com/ce/user/markdown.html#special-gitlab-references\n\n[issue-1]: https://gitlab.com/pawamoy/git-changelog/issues/1\n[issue-2]: https://gitlab.com/pawamoy/git-changelog/issues/2\n[issue-3]: https://gitlab.com/pawamoy/git-changelog/issues/3\n[issue-4]: https://gitlab.com/pawamoy/git-changelog/issues/4\n[issue-5]: https://gitlab.com/pawamoy/git-changelog/issues/5\n[issue-6]: https://gitlab.com/pawamoy/git-changelog/issues/6\n[issue-7]: https://gitlab.com/pawamoy/git-changelog/issues/7\n\n## Requirements\ngit-changelog requires Python 3.6 or above.\n\n<details>\n<summary>To install Python 3.6, I recommend using <a href="https://github.com/pyenv/pyenv"><code>pyenv</code></a>.</summary>\n\n```bash\n# install pyenv\ngit clone https://github.com/pyenv/pyenv ~/.pyenv\n\n# setup pyenv (you should also put these three lines in .bashrc or similar)\nexport PATH="${HOME}/.pyenv/bin:${PATH}"\nexport PYENV_ROOT="${HOME}/.pyenv"\neval "$(pyenv init -)"\n\n# install Python 3.6\npyenv install 3.6.8\n\n# make it available globally\npyenv global system 3.6.8\n```\n</details>\n\n## Installation\nWith `pip`:\n```bash\npython3.6 -m pip install git-changelog\n```\n\nWith [`pipx`](https://github.com/pipxproject/pipx):\n```bash\npython3.6 -m pip install --user pipx\n\npipx install --python python3.6 git-changelog\n```\n\n## Usage (command-line)\n```\nusage: git-changelog [-h] [-o OUTPUT] [-s {angular,atom,basic}]\n                     [-t {angular,keepachangelog}] [-v]\n                     REPOSITORY\n\nCommand line tool for git-changelog Python package.\n\npositional arguments:\n  REPOSITORY            The repository path, relative or absolute.\n\noptional arguments:\n  -h, --help            Show this help message and exit.\n  -o OUTPUT, --output OUTPUT\n                        Output to given file. Default: stdout.\n  -s {angular,atom,basic}, --style {angular,atom,basic}\n                        The commit style to match against.\n  -t {angular,keepachangelog}, --template {angular,keepachangelog}\n                        The Jinja2 template to use. Prefix with "path:" to\n                        specify the path to a directory containing a file\n                        named "changelog.md".\n  -v, --version         Show the current version of the program and exit.\n\n```\n',
    'author': 'Timothée Mazzucotelli',
    'author_email': 'pawamoy@pm.me',
    'url': 'https://github.com/pawamoy/git-changelog',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
