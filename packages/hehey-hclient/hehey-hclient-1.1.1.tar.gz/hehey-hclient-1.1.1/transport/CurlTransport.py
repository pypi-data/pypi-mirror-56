
from .Transport import Transport
import pycurl
from ..base.Request import Request
from io import BytesIO
from urllib.parse import urlencode
"""
 * curl 传输协议基类
 *<B>说明：</B>
 *<pre>
 *  使用
 *</pre>
 *<B>示例：</B>
 *<pre>
 * pycurl 文档
 * http://pycurl.io/docs/latest/index.html
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
class CurlTransport(Transport):

    def send(self,request):

        bufferBody = BytesIO()
        curl = self.prepare(request,bufferBody)
        curl.perform()
        response = request.getResponse()
        body = bufferBody.getvalue()
        response.setContent(body.decode('utf8'))
        response.setStatusCode(curl.getinfo(pycurl.HTTP_CODE))
        curl.close()

        return request


    def prepare(self,request:Request,bufferBody):

        request.prepare()
        curl = pycurl.Curl()
        # 设置超时时间
        curl.setopt(pycurl.CONNECTTIMEOUT, request.getTimeout())
        # 设置请求地址
        curl.setopt(pycurl.URL, request.getFullUrl())

        # 设置头部信息
        curl.setopt(pycurl.HTTPHEADER, request.formatHeaders())

        # 设置参数
        curl.setopt(curl.WRITEDATA, bufferBody)

        data = request.getParams();
        if isinstance(data,dict):
            data = urlencode(data).encode('utf-8')
        curl.setopt(curl.POSTFIELDS, data)

        return curl

    def batchSend(self, requests):
        curlMulti = pycurl.CurlMulti()
        curlResources = [];

        for (index,request) in requests.items():
            bufferBody = BytesIO()
            curl = self.prepare(request,bufferBody)

            curlMulti.add_handle(curl)
            curlResources.append({
                'bufferBody':bufferBody,
                'curl':curl,
                'request':request
            })

        # 批量请求
        while 1:
            ret, num_handles = curlMulti.perform()
            if ret != pycurl.E_CALL_MULTI_PERFORM:
                break

        while num_handles:
            ret = curlMulti.select(1.0)
            if ret == -1:
                continue

            while 1:
                ret, num_handles = curlMulti.perform()
                if ret != pycurl.E_CALL_MULTI_PERFORM: break

        for curlResource in curlResources:
            curl = curlResource['curl']
            request = curlResource['request']
            bufferBody = curlResource['bufferBody']
            response = request.getResponse()
            body = bufferBody.getvalue()
            response.setContent(body.decode('utf8'))
            response.setStatusCode(curl.getinfo(pycurl.HTTP_CODE))






