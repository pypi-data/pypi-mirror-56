#!/usr/bin/env python


import pytest
from lxml import etree

from chamelboots import ChameleonTemplate
from chamelboots import TalStatement
from chamelboots.cli import main
from chamelboots.constants import HTML_PARSER

RAISES_VALUE_ERROR = pytest.raises(ValueError)


def test_main():
    assert main([]) == 0


def test_get_attr_proxy():
    """Use instance of ChameleonTemplate as inner value."""
    element = ChameleonTemplate()
    with pytest.raises(AttributeError):
        element.foo


def test_tal_collection():
    """Use multiple tals to improve coverage."""
    # "<p tal:condition="request.message" tal:content="request.message" />"
    request = type("Request", (), {"message": "foo world"})()
    tal_statements = [
        TalStatement(name, value)
        for name, value in zip(("condition", "content"), ("request.message",) * 2)
    ]
    print(
        etree.tostring(
            etree.fromstring(
                ChameleonTemplate(tag="p", tal_statements=tal_statements).render(
                    request=request
                ),
                HTML_PARSER,
            ),
            method="html",
        )
    )
    request = type("Request", (), {"message": False})()
    assert not ChameleonTemplate(tag="p", tal_statements=tal_statements).render(
        request=request
    )


@pytest.mark.parametrize(
    "args,expectation",
    [
        (("repeat", "${repeat}"), RAISES_VALUE_ERROR),
        (("foo", "foo foo"), RAISES_VALUE_ERROR),
        (("foo", "repeat foo"), RAISES_VALUE_ERROR),
    ],
)
def test_no_tal_keywords(args, expectation):
    """Test that error is thrown if context_value or inner_content has a tal keyword in it or the tal is not valid."""
    with expectation:
        kwargs = dict(tal_statements=TalStatement(*args))
        ChameleonTemplate(**kwargs)


def test_str_repr():
    """Improve coverage"""
    ct = ChameleonTemplate()
    assert all((ct.__str__(), ct.__repr__()))
