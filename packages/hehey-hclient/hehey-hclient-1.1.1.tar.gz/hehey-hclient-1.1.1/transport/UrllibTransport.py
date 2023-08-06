
from .Transport import Transport
import urllib.request
from urllib.parse import urlencode
from ..base.Request import Request

"""
 * 传输协议基类
 *<B>说明：</B>
 *<pre>
 *  使用
 *</pre>
 *<B>示例：</B>
 *<pre>
 *  略
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
class UrllibTransport(Transport):

    def send(self,request):

        req = self.prepare(request)
        httpResponse = urllib.request.urlopen(req)
        response = request.getResponse()
        response.setContent(httpResponse.read().decode('utf8'))
        response.setStatusCode(httpResponse.getcode())

        return request


    def prepare(self,request:Request):

        request.prepare()
        data = request.getParams();
        if isinstance(data,dict):
            data = urllib.parse.urlencode(data).encode('utf-8')

        req = urllib.request.Request(url=request.getFullUrl(),data = data, method=request.getMethod())

        return req



