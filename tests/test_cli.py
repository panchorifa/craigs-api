"""
command line interface tests
"""
import os
from core import XRequests

BOSTON_SAMPLE_HTML = 'tests/samples/boston.html'
EXPECTED_TEXT = "[Jan 13] java: JAVA Developer  (Boston near North and South Station)"


def test_cli():
    cmd = 'python xlist.py find -X sof -K java -C boston -T {}'.format(BOSTON_SAMPLE_HTML)
    text = os.popen(cmd).read()
    assert(EXPECTED_TEXT in text)
