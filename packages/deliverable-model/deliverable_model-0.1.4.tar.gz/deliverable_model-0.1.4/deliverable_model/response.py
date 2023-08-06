from typing import List, Any


class Response(object):
    def __init__(self, data: List[Any]):
        self.data_history = []
        self.data = data

    def update_data(self, data):
        self.data_history.append(self.data)
        self.data = data
