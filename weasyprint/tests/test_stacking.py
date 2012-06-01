# coding: utf8
"""
    weasyprint.tests.stacking
    -------------------------

    :copyright: Copyright 2011-2012 Simon Sapin and contributors, see AUTHORS.
    :license: BSD, see LICENSE for details.

"""

from __future__ import division, unicode_literals

from ..stacking import StackingContext
from .test_layout import parse
from .testing_utils import (
    resource_filename, TestPNGDocument, assert_no_logs, capture_logs)


def to_lists(page):
    html, = page.children
    return serialize_stacking(StackingContext.from_box(html, page))


def serialize_box(box):
    return '%s %s' % (box.element_tag, box.sourceline)


def serialize_stacking(context):
    return (
        serialize_box(context.box),
        [serialize_box(b) for b in context.blocks_and_cells],
        [serialize_stacking(c) for c in context.zero_z_contexts],
    )


@assert_no_logs
def test_nested():
    page, = parse('''\
        <p id=lorem></p>
        <div style="position: relative">
            <p id=lipsum></p>
        </p>
    ''')
    assert to_lists(page) == (
        'html 1',
        ['body 1', 'p 1'],
        [(
            'div 2',
            ['p 3'],
            [])])