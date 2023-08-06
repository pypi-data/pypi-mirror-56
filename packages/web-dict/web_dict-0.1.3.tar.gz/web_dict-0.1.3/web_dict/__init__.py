from .core.factory import CollinsDictionary, OxfordDictionary
from .core.prviders.collinsdictionary import CollinsWeb
from .core.prviders.lexico import Lexico

LexicoDictionary = OxfordDictionary
__all__ = (CollinsDictionary, LexicoDictionary, OxfordDictionary, Lexico, CollinsWeb)
