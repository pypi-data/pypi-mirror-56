import unittest
from RookieTools import WebFileCheckBase
from RookieTools import downloader


class IndexCheck(WebFileCheckBase, unittest.TestCase):
    ThreadNumber = 1
    GetOneResult = True
    PluginName = 'IndexCheck'

    def tasks_init(self):
        [self.tasks.append(i) for i in ['/index.php', '/index.html', '/index.htm', '/default.htm', '/default.html',
                                        '/default.php']]

    def check(self, path):
        if self.GetOneResult and self.result:
            return

        target = self.url + path
        resp = downloader(target, stream=True)
        if resp is None:
            return False

        if resp.ok:
            self.result.append(target)
            return True

    def pipe(self, result):
        print(self.result)
        self.assertTrue(len(self.result) == 1)


if __name__ == '__main__':
    IndexCheck('http://www.baidu.com')