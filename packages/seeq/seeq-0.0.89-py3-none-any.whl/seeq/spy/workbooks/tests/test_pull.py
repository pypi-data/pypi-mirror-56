import pytest

from seeq import spy

from ...tests import test_common
from . import test_load

from ... import _login
from seeq.sdk43 import *

def setup_module():
    test_common.login()


@pytest.mark.monitors
def test_export_monitors_seeq_site():
    spy.login(url='https://explore.seeq.com', auth_token='TtEIO_wzTR5lNRGllrEBbw')
    print(Configuration().verify_ssl)

    search_df = spy.workbooks.search({
    }, recursive=True)

    workbooks = spy.workbooks.pull(search_df)

    spy.workbooks.save(workbooks, r'D:\Scratch\monitors_mark', clean=True)
