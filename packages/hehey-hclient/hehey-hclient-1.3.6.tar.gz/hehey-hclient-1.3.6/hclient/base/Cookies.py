
"""
 * http cookie信息对象
 *<B>说明：</B>
 *<pre>
 *  使用
 *</pre>
 *<B>示例：</B>
 *<pre>
 * 略
 *</pre>
 *<B>日志：</B>
 *<pre>
 *  略
 *</pre>
 *<B>注意事项：</B>
 *<pre>
 *  略
 *</pre>
"""
class Cookies(object):

    def __init__(self):

        self._cookies = {}

    def getCookies(self):

        return self._cookies

    def setCookies(self,cookies):

        self._cookies = cookies

    def set(self, name, value):
        name = self.formatName(name);
        self._cookies[name] = value

    def has(self, name):

        valueList = self._cookies.get(name, None)
        if valueList is None:
            return False
        else:
            return False

    def remove(self, name):

        self._cookies.pop(name)

        return True

    def removeAll(self):

        self._cookies = {};

        return True

    def getCount(self):

        return len(self._cookies)

    def formatName(self, name):

        return name.lower()

    def formatCookie(self):

        cookieList = []

        if not self._cookies:
            return ''

        for name, value in self._cookies.items():
            cookieList.append("{0}={1}".format(name, value))

        return ';'.join(cookieList);


    def __iter__(self):

        return self._cookies

    def __getitem__(self, key):

        return self._cookies.get(key, None)
