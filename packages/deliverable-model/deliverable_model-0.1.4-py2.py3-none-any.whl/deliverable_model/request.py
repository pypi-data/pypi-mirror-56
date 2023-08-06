from typing import List, Any


class Request(object):
    def __init__(self, query: List[Any]):
        self.query_history = []
        self.query = query

    def update_query(self, query):
        self.query_history.append(self.query)
        self.query = query
