import utils

class Query:
    def __init__(self, topid, title, description, narrative):
        self._topid = topid
        self._title = title
        self._description = description
        self._narrative = narrative

        self._distri = utils.distribution(title)
        self._vec = utils.vector(title)


