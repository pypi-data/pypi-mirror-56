import pytest

from groceries_app.wunderlist.config import WunderpyAccessEnvironmentVariables
from groceries_app.wunderlist.wunderlist import add_groceries_to_wunderlist


@pytest.mark.skip()
def test_wunderpy_add_groceries():
    target_list_name = 'test_list'
    groceries = [{'item': '2 kg mel', 'description': 'pizza'},
                 {'item': '10 wienerpølser', 'description': 'wienerpølser'}]
    config = WunderpyAccessEnvironmentVariables(client_id_var='WUNDERPY_CLIENT_ID', access_token_var='WUNDERPY_ACCESS_TOKEN')
    add_groceries_to_wunderlist(wunderlist_config=config, target_list_name=target_list_name, groceries=groceries)