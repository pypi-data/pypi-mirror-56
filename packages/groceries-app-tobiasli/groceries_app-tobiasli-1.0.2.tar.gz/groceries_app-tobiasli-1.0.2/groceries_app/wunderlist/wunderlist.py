import typing as ty

import wunderpy2

from groceries_app.wunderlist.config import WunderpyAccessBase, WunderpyAccessEnvironmentVariables


# To get wunderpy2 working, change iteritems() to items() in wunderpy2 code.

def add_groceries_to_wunderlist(wunderlist_config: WunderpyAccessBase, target_list_name: str,
                                groceries: ty.Sequence[ty.Dict[str, str]]):
    """With the given wunderlist_config, add groceries to target_list_name."""

    api = wunderpy2.WunderApi()
    client = api.get_client(wunderlist_config.access_token, wunderlist_config.client_id)

    lists = client.get_lists()

    target_list = None
    for li in lists:
        if li['title'] == target_list_name:
            target_list = li
            break

    if not target_list:
        print('Target list not found!')

    else:
        for item in groceries:
            task = client.create_task(target_list['id'], item['item'])
            client.create_note(task[wunderpy2.Task.ID], item['description'])

    return 'Wunderpy ok'



