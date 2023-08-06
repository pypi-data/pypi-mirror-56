import pytest

from seeq import spy

from ...tests import test_common
from . import test_load

from ... import _login
from seeq.sdk43 import *

def setup_module():
    test_common.login()


@pytest.mark.system8
def test_pull():
    spy.login(url='https://explore.seeq.com', auth_token='lByTzfAa6kWuRG_JRTyrXg', ignore_ssl_errors=True)

    workbooks = spy.workbooks.load(r'D:\Scratch\MarkWorkbookTest')

    spy.workbooks.push(workbooks, path='MarkD Import Test - Pharma Use Cases', label='MarkD')


@pytest.mark.monitors
def test_export_monitors_seeq_site():
    spy.login(url='https://monitors.seeq.site', auth_token='Yre09-GgdtOxN9wSkkbQ_A')

    search_df = spy.workbooks.search({
        'Path': 'Exxon',
        'Name': '/^Exxon Topic$/',
        'Workbook Type': 'Topic'
    }, recursive=True, content_filter='ALL')

    workbooks = spy.workbooks.pull(search_df)

    spy.workbooks.save(workbooks, r'D:\Scratch\monitors_mark', clean=True)
