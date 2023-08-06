# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['pelican', 'pelican.plugins.add_css_classes']

package_data = \
{'': ['*']}

install_requires = \
['beautifulsoup4>=4.8,<5.0',
 'pelican>=4.2,<5.0',
 'toml>=0.10.0,<0.11.0',
 'typing-extensions>=3.7,<4.0']

extras_require = \
{'markdown': ['markdown>=3.1.1,<4.0.0']}

setup_kwargs = {
    'name': 'pelican-add-css-classes',
    'version': '1.0.0',
    'description': 'Adds CSS classes to html tags in Pelican documents',
    'long_description': '# Add css classes: A Plugin for Pelican\n\nAdds CSS classes to html tags in Pelican documents\n\nInstallation\n------------\n\nThis plugin can be installed via:\n\n    pip install pelican-add-css-classes\n\nContributing\n------------\n\nContributions are welcome and much appreciated. Every little bit helps. You can contribute by improving the documentation, adding missing features, and fixing bugs. You can also help out by reviewing and commenting on [existing issues][].\n\nTo start contributing to this plugin, review the [Contributing to Pelican][] documentation, beginning with the **Contributing Code** section.\n\n[existing issues]: https://github.com/johanvergeer/pelican-add-css-classes/issues\n[Contributing to Pelican]: https://docs.getpelican.com/en/latest/contribute.html\n',
    'author': 'Johan Vergeer',
    'author_email': 'johanvergeer@gmail.com',
    'url': 'https://github.com/johanvergeer/pelican-add-css-classes',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
