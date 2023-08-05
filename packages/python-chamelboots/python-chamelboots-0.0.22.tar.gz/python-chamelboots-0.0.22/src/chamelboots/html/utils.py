"""Define html utilities."""

from bs4 import BeautifulSoup


def prettify_html(html_string):
    """Make :html_string: pretty."""

    return BeautifulSoup(html_string, "html.parser").prettify()
