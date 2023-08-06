import json
import unittest

from web_dict.core.prviders.collinsdictionary import CollinsWeb


class CollinsTest(unittest.TestCase):

    def test_spanish_1(self):
        c = CollinsWeb('hacer')
        #self._p(c)

    def test_spanish_2(self):
        c = CollinsWeb('cómo')
        self._p(c)

    def test_english_1(self):
        c = CollinsWeb('INTRANSITIVE', 'english')
        #self._p(c)

    def _p(self, c):
        print(json.dumps(c.to_dict(), indent=4, ensure_ascii=False))


if __name__ == '__main__':
    unittest.main()
