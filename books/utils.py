import json
import urllib.request
from urllib.error import HTTPError


def lobid_to_data(gnd_id):
    if gnd_id is not None:
        try:
            with urllib.request.urlopen(gnd_id) as url:
                data = json.loads(url.read().decode())
        except HTTPError:
            data = None
            print("ERROR: {}".format(gnd_id))
        return data
    else:
        return None
