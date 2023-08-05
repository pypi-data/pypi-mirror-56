# -*- coding: utf-8 -*-
from distutils.core import setup

package_dir = \
{'': 'src'}

packages = \
['calender',
 'calender.migrations',
 'films',
 'films.clients',
 'films.core',
 'films.migrations',
 'films.templatetags',
 'schedule',
 'schedule.migrations',
 'vote4film',
 'votes',
 'votes.migrations',
 'web']

package_data = \
{'': ['*'],
 'calender': ['templates/calender/*'],
 'films': ['templates/films/*'],
 'schedule': ['templates/schedule/*'],
 'votes': ['templates/votes/*', 'templates/votes/includes/*'],
 'web': ['templates/web/*']}

modules = \
['manage']
install_requires = \
['django-environ>=0.4.5,<0.5.0',
 'django-extensions>=2.2,<3.0',
 'django>=2.2,<3.0',
 'lxml>=4.4,<5.0',
 'requests>=2.22,<3.0',
 'xdg>=4.0,<5.0']

extras_require = \
{'postgres': ['psycopg2>=2.8,<3.0']}

entry_points = \
{'console_scripts': ['manage = manage:main']}

setup_kwargs = {
    'name': 'vote4film',
    'version': '1.1.0',
    'description': 'Easy scheduling for regular film nights',
    'long_description': '# Vote4Film\n\nSimplify film selection for regular film nights. Participants can:\n\n- Add films\n- Vote for films\n- Declare absences\n- See the schedule which takes into account votes and absences\n\nAdmins can set the schedule of film nights.\n\nThis is a simple WSGI Web Application. The back-end is Django, and the front-end\nis dynamic HTML served by Django (no JavaScript is used).\n\n## Development\n\n1. `poetry install` to set-up the virtualenv (one-off)\n2. `poetry run ./src/vote4film/manage.py migrate` to set-up the local DB (one-off)\n3. `poetry run ./src/vote4film/manage.py runserver_plus`\n4. `make fix`, `make check` and `make test` before committing\n\n### Contributing\n\nPull requests are welcome :)\n\n### Publishing\n\nThis application is published on PyPi.\n\n1. Ensure you have configured the PyPi repository with Poetry (one-off)\n2. Add the release notes in this README.md\n3. `poetry bump minor` to bump the major/minor/patch version\n4. `poetry publish --build` to release\n\nTo publish to the test repository:\n\n1. Ensure you have configured the Test PyPi repository with Poetry (one-off)\n2. `poetry publish --build -r testpypi` to upload to the test repository\n\n## Deployment\n\nUnfortunately, I will not provide detailed guidance for production deployment.\n\nSome general tips:\n\n* Create a virtualenv, e.g. in `~/virtualenv`\n* Install with `pip install vote4film[postgres]`\n* Write the configuration at `~/.config/vote4film/local.env`\n* Use Postgres as the database\n* Use Nginx/uWSGI to to serve the site (with HTTPS)\n* Run Django management commands using `./virtualenv/bin/manage`\n\n## Changelog\n\n### v1.1.0 - 2019/11/16\n\n- Show the register of present/absent users for upcoming films\n- Fix not highlighting films that are not available to be watched\n- Fix parsing of "Not Rated" age ratings resulting in an error\n\n### v1.0.9 - 2019/11/13\n\n- Actually let\'s not be too dumb about packaging\n\n### v1.0.8 - 2019/11/13\n\n- Rename management command from vote4film to manage\n- Stop trying to be smart about packaging\n\n### v1.0.7 - 2019/11/13\n\n- The same fixes as v1.0.6 but for real this time\n\n### v1.0.6 - 2019/11/13\n\n- Fix url patterns for internal apps in installed environment\n- Fix missing template files in PyPi package (so typical!)\n\n### v1.0.5 - 2019/11/12\n\n- Add optional postgres support, e.g. `pip install vote4film[postgres]`\n\n### v1.0.4 - 2019/11/12\n\n- Fix bug loading config from XDG config home (sigh)\n- Fix django-extensions being missed from dependencies\n\n### v1.0.3 - 2019/11/12\n\n- Fix config sub-directory used in XDG config home\n\n### v1.0.2 - 2019/11/12\n\n- Load configuration from XDG config home\n\n### v1.0.1 - 2019/11/10\n\n- First release of Vote4Film\n',
    'author': 'QasimK',
    'author_email': 'noreply@QasimK.io',
    'url': 'https://github.com/Fustra/vote4film/',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'py_modules': modules,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
