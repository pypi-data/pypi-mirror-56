
"""
 * http 头部信息对象
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
class Headers(object):

    def __init__(self):

        self._headers = {}


    def getHeaders(self):

        return self._headers

    def setHeaders(self,headers):

        self._headers = headers

    def set(self,name,value):

        name = self.formatName(name);
        self._headers[name] = [value]

        return True;

    def add(self,name,value):

        name = self.formatName(name);
        valueList = self._headers.get(name,None)

        if valueList is None:
            valueList = [value]
        else:
            valueList.append(value)

        self._headers[name] = valueList

        return True;

    def has(self,name):

        valueList = self._headers.get(name, None)
        if valueList is None:
            return False
        else:
            return False

    def remove(self,name):

        self._headers.pop(name)

        return True

    def removeAll(self):

        self._headers = {};

        return True

    def getCount(self):

        return len(self._headers)

    def formatName(self,name):

        return name.lower()

    def formatHeader(self):

        headerList = []

        if self._headers:
            for name,value in self._headers.items():
                if isinstance(value,list):
                    headerList.append("{0}: {1}".format(name,';'.join(value)))
                else:
                    headerList.append("{0}: {1}".format(name,value))

        return headerList;

    def __iter__(self):

        return self._headers

    def __getitem__(self,name):

        name = self.formatName(name);

        return self._headers.get(name,None)