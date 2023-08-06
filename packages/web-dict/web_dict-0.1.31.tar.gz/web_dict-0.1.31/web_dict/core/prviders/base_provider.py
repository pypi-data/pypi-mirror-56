import abc

from ..parser import WebParser


class BaseProvider(WebParser):
    to_dict_fields = ('head_word',)

    def __init__(self, word: str, seg: str):
        super(BaseProvider, self).__init__(word, )
        self.seg = seg

    @property
    @abc.abstractmethod
    def head_word(self):
        ...
