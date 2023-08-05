# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['measurement',
 'measurement.plugins',
 'measurement.plugins.download_speed',
 'measurement.plugins.download_speed.tests',
 'measurement.plugins.latency',
 'measurement.plugins.latency.tests']

package_data = \
{'': ['*']}

install_requires = \
['six>=1.12,<2.0', 'validators>=0.13.0,<0.14.0']

extras_require = \
{':python_version == "3.6"': ['dataclasses>=0.6.0,<0.7.0']}

setup_kwargs = {
    'name': 'honestybox-measurement',
    'version': '1.0.2',
    'description': 'A framework for measuring things and producing structured results.',
    'long_description': "# honestybox-measurement\n\nA framework for measuring things and producing structured results.\n\n## Requirements\n\n`honestybox-measurement` supports Python 3.5 to Python 3.8 inclusively.\n\n\n## Releases\n\nTo ensure releases are always built on the latest codebase, *changes are only ever merged from master*.\n\n### Creating a release\n1. Ensure that master is up to date:\n\n    ```shell script\n    git checkout master\n    git pull origin\n    ```\n\n2. Switch to release and ensure it is up to date:\n\n    ```shell script\n    git checkout release\n    git pull origin\n    ```\n\n3. Merge from master:\n\n    ```shell script\n    git merge master\n    ```\n\n4. Add a new release to CHANGELOG.md and include all changes in [Unreleased].\n\n5. Update version number in `pyproject.toml`\n\n6. Commit the changes to the `release` branch with comment `Release <version number>`\n\n    ```shell script\n    git add CHANGELOG.md pyproject.toml\n    git commit -m 'Release 0.0.1`\n    ```\n\n7. Tag the commit with the release number:\n\n    ```shell script\n     git tag 0.0.1\n    ```\n\n8. Push the commit and tags upstream:\n\n    ```shell script\n    git push && git push --tags\n    ```\n\n9. Merge changes into master and push upstream:\n\n    ```shell script\n    git checkout master\n    git merge release\n    git push\n    ```\n\n\n### Publishing a release\n\n1. Install [poetry](https://poetry.eustace.io) \n\n2. Checkout the release:\n\n    ```shell script\n    git checkout 0.0.1\n    ```\n\n3. Publish the release:\n\n    ```shell script\n    poetry publish --build\n    ```\n",
    'author': 'Honesty Box',
    'author_email': 'engineering@honestybox.com.au',
    'url': 'https://github.com/honesty-box/honestybox-measurement/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.5',
}


setup(**setup_kwargs)
