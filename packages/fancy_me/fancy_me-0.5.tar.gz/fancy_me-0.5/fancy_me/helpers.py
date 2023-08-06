import json
class MetaData:

    def __init__(self, **kwargs):
        self.data = kwargs

    @property
    def user(self):
        return self.data['data']['user']


class Message:
    def __init__(self, type: str, data: dict):
        self._data = data
        self._type = type

    @property
    def message(self):
        return f"{self._type}>{json.dumps(self._data)}"

    def __repr__(self):
        # return send()
        return f"data_type = {self._type}"
