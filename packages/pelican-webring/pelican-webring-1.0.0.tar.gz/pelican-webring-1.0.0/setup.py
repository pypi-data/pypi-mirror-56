# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['pelican', 'pelican.plugins.webring']

package_data = \
{'': ['*'], 'pelican.plugins.webring': ['test_data/*']}

install_requires = \
['feedparser>=5.2,<6.0', 'pelican>=4.2,<5.0']

extras_require = \
{'markdown': ['markdown>=3.1.1,<4.0.0']}

setup_kwargs = {
    'name': 'pelican-webring',
    'version': '1.0.0',
    'description': 'Adds a webring to your site from a list of web feeds',
    'long_description': '# Webring\n\n[![Build Status](https://github.com/pelican-plugins/webring/workflows/build/badge.svg)](https://github.com/pelican-plugins/webring/actions)\n\nThis Pelican plugin adds a webring to your site from a list of web feeds.\n\nIt retrieves the latest posts from a list of web feeds and makes them available\nin templates, effectively creating a [partial webring][1]. Posts are sorted\nfrom newer to older.\n\nIt is inspired by [openring](https://git.sr.ht/~sircmpwn/openring), a tool for\ngenerating an HTML file to include in your [SSG][2] from a template and a list of\nweb feeds.\n\nInstallation\n------------\n\nThis plugin can be installed via:\n\n    pip install pelican-webring\n\nSettings\n--------\n\n```\nWEBRING_FEED_URLS = []\n```\nA list of web feeds in the form of a URL or local file.\n\n```\nWEBRING_MAX_ARTICLES = 3\n```\nThe maximum number of articles.\n\n```\nWEBRING_ARTICLES_PER_FEED = 1\n```\nThe maximum number of articles per feed.\n\n```\nWEBRING_SUMMARY_LENGTH = 128\n```\nThe maximum length of post summaries.\n\n```\nWEBRING_CLEAN_SUMMARY_HTML = True\n```\nWhether to clean html tags from post summaries or not.\n\n**Example**\n\nLet\'s suppose we have two blogs in our webring and want to show two articles\nper blog. We would also like to show a quite short summary.\n\n```\nWEBRING_FEED_URLS = [\n    \'https://justinmayer.com/feeds/all.atom.xml\',\n    \'https://danluu.com/atom.xml\'\n]\nWEBRING_ARTICLES_PER_FEED = 2\nWEBRING_MAX_ARTICLES = 4\nWEBRING_SUMMARY_LENGTH = 25\n```\n\nTemplates\n---------\n\nThe plugin makes available the resulting web feed articles in the variable\n`webring_articles`, which is a list of `Article` objects whose attributes are:\n\n- `title`: The article title.\n- `link`: The article URL.\n- `date`: The article date as a Pelican `utils.SafeDatetime` object, which can\nbe used with [Pelican\'s Jinja filter `strftime`](https://docs.getpelican.com/en/stable/themes.html#date-formatting).\n- `summary`: The article summary, as provided in the web feed and modified\naccording to this plugin\'s settings.\n- `source_title`: The title of the web feed.\n- `source_link`: A link to the web feed.\n- `source_id`: An identification field provided in some web feeds.\n\nSee the following section for an example on how to iterate the article list.\n\n**Example**\n\nImagine we\'d like to put our webring in the bottom of the default Pelican\ntemplate (ie. notmyidea). To simplify, we\'ll use the existing CSS classes.\n\nEdit the `notmyidea/templates/base.html` file and make it look like this:\n\n```\n        ...\n        <section id="extras" class="body">\n        {% if WEBRING_FEED_URLS %}\n            <div class="webring">\n                <h2>Webring</h2>\n                {% for article in webring_articles %}\n                <p><a href="{{ article.link }}">{{ article.title }}</a></p>\n                <p>{{ article.date|strftime(\'%d %B %Y\') }} - {{ article.summary}}</p>\n                {% endfor %}\n            </div>\n        {% endif %}\n        {% if LINKS %}\n        ...\n```\n\nIf there were no links or social widgets, the result would be like in the\nimage below:\n\n![Example of Webring](https://github.com/pelican-plugins/webring/raw/master/example.png)\n\nContributing\n------------\n\nContributions are welcome and much appreciated. Every little bit helps. You can contribute by improving the documentation, adding missing features, and fixing bugs. You can also help out by reviewing and commenting on [existing issues][].\n\nTo start contributing to this plugin, review the [Contributing to Pelican][] documentation, beginning with the **Contributing Code** section.\n\n[existing issues]: https://github.com/pelican-plugins/webring/issues\n[Contributing to Pelican]: https://docs.getpelican.com/en/latest/contribute.html\n[1]: https://en.wikipedia.org/wiki/Webring "In a proper webring, websites would be linked in a circular structure."\n[2]: https://en.wikipedia.org/wiki/Category:Static_website_generators "Static Site Generator"\n\n',
    'author': 'David Alfonso',
    'author_email': 'developer@davidalfonso.es',
    'url': 'https://github.com/pelican-plugins/webring',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
