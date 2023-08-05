import requests

API_URL = "https://tchk83fgka.execute-api.eu-west-1.amazonaws.com/staging/api/v1/push"


class PythonPlugin:
    """
    A python plugin to send data(json) from any data platform to a connected API.
    """

    def __init__(self):
        pass

    def send_data(self, data_container):
        """send the data to the API."""

        if type(data_container) == list:
            payload = {
                "data": [
                    {
                        "source": single_data['data_source'],
                        "type": single_data['data_type'],
                        "payload": single_data['data']
                    } for single_data in data_container
                ]
            }

        elif type(data_container) == dict:

            payload = {
                "data": {
                    "source": data_container['data_source'],
                    "type": data_container['data_type'],
                    "payload": data_container['data']
                }
            }

        else:
            raise TypeError("Invalid data container")

        try:
            r = requests.post(url=API_URL, json=payload)

        except BaseException as e:
            raise e

        else:
            return r.status_code
