import json
import unittest

from web_dict.core.factory import CollinsDictionary, OxfordDictionary


class CollinsTest(unittest.TestCase):

    def test_collins(self):
        with CollinsDictionary(word='hacer') as c:
            self._p(c.es2en())

    def rtest_oxford(self):
        c = OxfordDictionary()
        self._p(
            c.es2en('hacer')
        )

    def _p(self, c):
        print(json.dumps(c, ensure_ascii=False, indent=4))


if __name__ == '__main__':
    unittest.main()
