"""Convert HTML to a nested dict of dicts and arrays."""
from lxml import etree

from ..constants import HTML_PARSER

INNER_CONTENT, ATTRIBS, ATTRIBUTES, TAIL = (
    "inner_content",
    "attribs",
    "attributes",
    "tail",
)


def dictdata(node):
    res = {}
    res[node.tag] = []
    html_to_dict(node, res[node.tag])
    reply = {}
    reply[node.tag] = {
        INNER_CONTENT: res[node.tag],
        ATTRIBS: node.attrib,
        TAIL: node.tail,
    }
    return reply


def html_to_dict(node, res):
    rep = {}
    if len(node):
        for n in list(node):
            rep[node.tag] = []
            value = html_to_dict(n, rep[node.tag])
            if len(n):

                value = {
                    INNER_CONTENT: rep[node.tag],
                    ATTRIBUTES: n.attrib,
                    TAIL: n.tail,
                }
                res.append({n.tag: value})
            else:
                res.append(rep[node.tag][0])
    else:
        value = {}
        value = {INNER_CONTENT: node.text, ATTRIBUTES: node.attrib, TAIL: node.tail}
        res.append({node.tag: value})
    return None


def get_html_as_data(html_string):
    """Convert HTML string into nested dict of data."""
    return dictdata(etree.fromstring(html_string, HTML_PARSER).getroottree().getroot())
