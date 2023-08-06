# -*- coding: utf-8 -*-

from ..utils.ClientUtil import ClientUtil
from .Response import Response
from ..protocol.ServiceResponse import ServiceResponse
from ..format.Formatter import Formatter
from .Headers import Headers
from .Cookies import Cookies
import re
from urllib.parse import urlparse,urlencode
"""
 * 请求类
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
class Request(object):
    '''
        :type client: hclient.client.Client
    '''
    def __init__(self,attrs = {}):

        # 请求地址
        # <B> 说明： </B>
        # <pre>
        # 不包含host
        # </pre>
        self.url = '';

        # 请求host
        # <B> 说明： </B>
        # <pre>
        # 略
        # </pre>
        self.host = '';

        # 80 端口
        # <B> 说明： </B>
        # <pre>
        # 略
        # </pre>
        self.port = 80;

        # 套接字类型
        # <B> 说明： </B>
        # <pre>
        # 略
        # </pre>
        self.scheme = 'tcp'

        # 完整地址
        # <B> 说明： </B>
        # <pre>
        # 略
        # </pre>
        self.fullUrl = ''

        # 请求方法
        # <B> 说明： </B>
        # <pre>
        # 略
        # </pre>
        self.method = 'GET'

        # 客户端
        # <B> 说明： </B>
        # <pre>
        # 略
        # </pre>
        self.client = None

        # 头部对象
        # <B> 说明： </B>
        # <pre>
        # 略
        # </pre>
        self.headers = None;

        # cookies 对象
        # <B> 说明： </B>
        # <pre>
        # 略
        # </pre>
        self.cookies = None;

        # 内容
        # <B> 说明： </B>
        # <pre>
        # 略
        # </pre>
        self.content = None;

        # 数据
        # <B> 说明： </B>
        # <pre>
        # 略
        # </pre>
        self.data = {}

        # 数据格式
        # <B> 说明： </B>
        # <pre>
        # 略
        # </pre>
        self.format = None

        # response 返回数据格式
        # <B> 说明： </B>
        # <pre>
        # 略
        # </pre>
        self.rformat = None

        # 对应的响应对象
        # <B> 说明： </B>
        # <pre>
        # 略
        # </pre>
        self.response = {}

        # 对应的响应对象
        # <B> 说明： </B>
        # <pre>
        # 略
        # </pre>
        self._response = None

        # 请求超时
        # <B> 说明： </B>
        # <pre>
        # 单位秒
        # </pre>
        self.timeout = 0;

        # 传输协议类
        # <B> 说明： </B>
        # <pre>
        # 略
        # </pre>
        self.transport = None

        if attrs:
            ClientUtil.setAttrs(self,attrs)


    def setClient(self,client):

        self.client = client

        return self;

    def setTimeout(self,timeout):

        self.timeout = timeout

        return self;

    def getTimeout(self):

        return self.timeout;

    # 获取响应对象
    # <B> 说明： </B>
    # <pre>
    # 略
    # </pre>
    def getResponse(self)->'Response':

        if self._response is None:
            responseConf = self.response.copy();
            responseConf['format'] = responseConf.get('format',self.rformat)
            self._response = self.client.createResponse(responseConf)
            self._response.setRequest(self)

        return self._response

    # 获取传输协议对象
    # <B> 说明： </B>
    # <pre>
    # 略
    # </pre>
    def getTransport(self):

        return self.transport

    # 设置请求内容
    # <B> 说明： </B>
    # <pre>
    # 略
    # </pre>
    def setContent(self, content):

        self.content = content

        return self

    # 设置数据
    # <B> 说明： </B>
    # <pre>
    # 略
    # </pre>
    def setData(self, data):

        self.data = data

        return self

    # 设置数据格式
    # <B> 说明： </B>
    # <pre>
    # 略
    # </pre>
    def setFormat(self, format):

        self.format = format

        return self

    def setMethod(self,method):

        self.method = method

        return self

    def getMethod(self):

        return self.method

    # 获取url
    # <B> 说明： </B>
    # <pre>
    # 略
    # </pre>
    def getUrl(self):

        return self.url

    # 设置url
    # <B> 说明： </B>
    # <pre>
    # 略
    # </pre>
    def setUrl(self,url):

        self.url = url

        return self

    # 设置host
    # <B> 说明： </B>
    # <pre>
    # 略
    # </pre>
    def setHost(self,host):

        self.host = host

        return self

    # 获取完整的地址
    # <B> 说明： </B>
    # <pre>
    # 略
    # </pre>
    def getFullUrl(self):

        return self.fullUrl

    def setFullUrl(self,fullUrl):

        self.fullUrl = fullUrl

    def getHost(self):

        return self.host

    def getPort(self):

        return self.port

    def getScheme(self):

        return self.scheme

    def getFormat(self)->'Formatter':

        return self.client.getFormatter(self.format)

    def getData(self):

        return self.data

    def getContent(self):

        return self.content

    def getParams(self):

        if self.content:
            return self.content

        if self.format:
            formatter = self.getFormat()
            formatter.format(self)
        else:
            self.content = self.data

        return self.content

    def addHeaders(self, key, value):
        self.getHeaders().set(key,value)

        return self;

    def addCookie(self,key,value):
        self.getCookies().set(key, value)

        return self

    def getHeaders(self)->Headers:

        if self.headers is None:
            self.headers = Headers()

        return self.headers

    def setHeaders(self,header):

        headers = self.getHeaders();
        headers.setHeaders(header)

        return self

    def getCookies(self)->'Cookies':

        if self.cookies is None:
            self.cookies = Cookies()

        return self.cookies

    def setCookies(self,cookies):

        cookies = self.getCookies();
        cookies.setCookies(cookies)

        return self

    # 发送请求
    # <B> 说明： </B>
    # <pre>
    # 略
    # </pre>
    def send(self)->'ServiceResponse':

        return self.client.send(self);

    # 格式化请求header
    # <B> 说明： </B>
    # <pre>
    # 略
    # </pre>
    def formatHeaders(self):
        headerList = []
        # cookies
        headers = self.getHeaders();

        # cookies
        cookies = self.getCookies();
        cookieLine = cookies.formatCookie()
        if cookieLine:
            headers.set('cookie',cookieLine)

        headerLine = headers.formatHeader();
        if headerLine:
            headerList = headerList + headerLine

        return headerList

    # 请求之前准备操作
    # <B> 说明： </B>
    # <pre>
    # 略
    # </pre>
    def prepare(self):

        # 地址处理
        if not self.fullUrl:
            if re.match(r'^https?:\/\/', self.getUrl(),re.IGNORECASE) is None:
                self.setFullUrl(self.getHost() + self.getUrl())
            else:
                self.setFullUrl(self.getUrl())

        # 数据处理
        content = self.getContent();
        if content is None:
            if self.format:
                formatter = self.getFormat()
                formatter.format(self)
            else:
                self.content = urlencode(self.data)

    # 构建请求所有内容
    # <B> 说明： </B>
    # <pre>
    # 略
    # </pre>
    def buildRequestContent(self):

        pass

    # 根据原始响应内容创建response
    # <B> 说明： </B>
    # <pre>
    # 略
    # </pre>
    def createResponse(self,responseRawContent:str)->'Response':

        # 默认解析为http 协议
        response = self.getResponse();

        headers = ''
        content = ''
        if responseRawContent:
            responseRawContentList = responseRawContent.split('\r\n\r\n',1)
            headers = responseRawContentList[0];
            content = responseRawContentList[1];

        response.setContent(content)
        response.setHeaders(headers.split('\r\n'))

        return response

