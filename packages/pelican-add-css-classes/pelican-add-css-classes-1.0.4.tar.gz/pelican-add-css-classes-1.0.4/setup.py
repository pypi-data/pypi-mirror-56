# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['pelican', 'pelican.plugins.add_css_classes']

package_data = \
{'': ['*']}

install_requires = \
['beautifulsoup4>=4.8,<5.0', 'pelican>=4.2,<5.0', 'toml>=0.10.0,<0.11.0']

extras_require = \
{'markdown': ['markdown>=3.1.1,<4.0.0']}

setup_kwargs = {
    'name': 'pelican-add-css-classes',
    'version': '1.0.4',
    'description': 'Adds CSS classes to html tags in Pelican documents',
    'long_description': '# Add css classes: A Plugin for Pelican\n\nAdds CSS classes to html tags in Pelican documents\n\n## Motivation\n\nWhen we want to create a page or article we often use Markdown or RST. This allows us to\nwrite content very fast, but it gives us little to no control over the styling of our page.\n\nThat is why I created this plugin for Pelican so we can add classes to HTML elements \ninside `pelicanconf.py`.\n\n## Usage\n\n### Both pages and articles\n\nTo set css classes that should be added to elements in both \npages and articles you can use `ADD_CSS_CLASSES`.\n\nYou can also set which css classes should be added to elements \non pages with `ADD_CSS_CLASSES_TO_PAGE`.\n\nAnd this can also be done with articles using `ADD_CSS_CLASSES_TO_ARTICLE`.\n\n#### Example\n\nLet\'s say you want to configure all tables to use Bootstrap, show black tables on pages \nand red headers on articles.\n\n```python\nADD_CSS_CLASSES = {\n    "table": ["table"]\n}\n\nADD_CSS_CLASSES_TO_PAGE = {\n    "table": ["table", "table-dark"]\n}\n\nADD_CSS_CLASSES_TO_ARTICLE = {\n    "h1": ["text-danger"]\n}\n```\n\nInstallation\n------------\n\nThis plugin can be installed via:\n\n    pip install pelican-add-css-classes\n\nContributing\n------------\n\nContributions are welcome and much appreciated. Every little bit helps. You can contribute by improving the documentation, adding missing features, and fixing bugs. You can also help out by reviewing and commenting on [existing issues][].\n\nTo start contributing to this plugin, review the [Contributing to Pelican][] documentation, beginning with the **Contributing Code** section.\n\n[existing issues]: https://github.com/johanvergeer/pelican-add-css-classes/issues\n[Contributing to Pelican]: https://docs.getpelican.com/en/latest/contribute.html\n',
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
