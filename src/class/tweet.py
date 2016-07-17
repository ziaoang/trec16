import utils

class Tweet:
    def __init__(self, text):
        self._text = text

        self._distri = utils.distribution(text)
        self._vec = utils.vector(text)


