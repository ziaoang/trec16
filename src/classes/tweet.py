import utils

class Tweet:
    def __init__(self, id, timestamp, text):
        self._id = id
        self._timestamp = timestamp
        self._text = text

        self._distri = utils.distribution(text)
        self._vec = utils.vector(text)


