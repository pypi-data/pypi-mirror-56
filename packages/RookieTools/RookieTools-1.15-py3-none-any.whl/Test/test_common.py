import unittest
from RookieTools import downloader, get_charset, host2ip, is_open_port


class TestCommon(unittest.TestCase):
    def str_check(self, r, s):
        self.assertIsInstance(r, str)
        self.assertEqual(r, s)

    def test_downloader(self):
        resp = downloader('http://www.baidu.com')
        self.assertIsNotNone(resp)
        self.assertTrue(resp.ok)

    def test_get_charset(self):
        resp = downloader('http://www.baidu.com')
        self.assertIsNotNone(resp)
        res = get_charset(resp)
        self.str_check(res, 'utf-8')

    def test_host2ip(self):
        res = host2ip('localhost')
        self.str_check(res, '127.0.0.1')

        self.assertTrue(is_open_port(host2ip('www.baidu.com'), 80))


if __name__ == '__main__':
    unittest.main()
