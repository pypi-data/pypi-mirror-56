"""Test the utilities."""
from chamelboots.datautils import get_from
from chamelboots.datautils import paths_from
from chamelboots.html import get_html_as_data
from chamelboots.html.packages.bootstrap import starter_html
from chamelboots.html.utils import prettify_html


def test_pretty_print_html():
    """Pretty print html."""

    data = get_html_as_data(prettify_html(starter_html))
    assert isinstance(data, dict)

    paths = paths_from(data)
    assert all(isinstance(item, tuple) for item in paths)
    assert len([get_from(data, path) for path in paths])
    assert all(all(str(item) for item in path) for path in paths)
