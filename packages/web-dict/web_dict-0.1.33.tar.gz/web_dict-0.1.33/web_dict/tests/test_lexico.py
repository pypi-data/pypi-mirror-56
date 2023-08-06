import json
import unittest

from web_dict.core.prviders.lexico import Lexico


class CollinsTest(unittest.TestCase):

    # def test_spanish_1(self):
    #     c = Lexico('dia',)
    #     self._p(c)

    def test_es_1(self):
        c = Lexico('prueba', 'es')
        self._p(c)

    # def test_english_1(self):
    #     c = Lexico('test', 'en')
    #     self._p(c)

    def _p(self, c):
        print(json.dumps(c.to_dict(), indent=4, ensure_ascii=False))


if __name__ == '__main__':
    unittest.main()
