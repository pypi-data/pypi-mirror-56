# -*- coding: utf-8 -*-
from ..utils.ClientUtil import ClientUtil
from ..format.Parser import Parser
from .Headers import Headers

"""
 * 请求响应类
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
class Response(object):


    def __init__(self,attrs = {}):

        # 响应的原始内容
        # <B> 说明： </B>
        # <pre>
        # 略
        # </pre>
        self.content = None;

        # 头部对象
        # <B> 说明： </B>
        # <pre>
        # 略
        # </pre>
        self.headers = None;

        # 格式化后的数据
        # <B> 说明： </B>
        # <pre>
        # 略
        # </pre>
        self.data = None

        # 数据格式类型
        # <B> 说明： </B>
        # <pre>
        # 略
        # </pre>
        self.format = None

        # http 状态码
        # <B> 说明： </B>
        # <pre>
        # 略
        # </pre>
        self.statusCode = None

        # 是否有网络错误
        # <B> 说明： </B>
        # <pre>
        # 略
        # </pre>
        self.networkError = None

        # 对应的请求对象
        # <B> 说明： </B>
        # <pre>
        # 略
        # </pre>
        self.request = None

        # 客户端
        # <B> 说明： </B>
        # <pre>
        # 略
        # </pre>
        self.client = None;

        # 获取信息
        # <B> 说明： </B>
        # <pre>
        # 略
        # </pre>
        self.errors = [];

        if attrs:
            ClientUtil.setAttrs(self,attrs)


    def setClient(self,client):

        self.client = client

    def setRequest(self,request):

        self.request = request;

    def getRequest(self):

        return self.request

    # 设置返回内容
    # <B> 说明： </B>
    # <pre>
    # 略
    # </pre>
    def setContent(self, content):

        self.content = content

    # 获取返回内容
    # <B> 说明： </B>
    # <pre>
    # 略
    # </pre>
    def getContent(self):

        return self.content

    def getHeaders(self)->Headers:

        if self.headers is None:
            self.headers = Headers()

        return self.headers

    def setHeaders(self,header):

        headers = self.getHeaders();
        headers.setHeaders(header)

        return self

    def getParser(self)->'Parser':

        return self.client.getParser(self.format)

    # 设置数据格式
    # <B> 说明： </B>
    # <pre>
    # 略
    # </pre>
    def setFormat(self, format):

        self.format = format

        return self

    def getData(self)->'dict':

        if self.data is not None:
            return self.data

        if self.format:
            self.getParser().format(self)
            return self.data
        else:
            return self.getContent()

    def setData(self,data):

        self.data = data

    def getStatusCode(self):

        return self.statusCode

    def setStatusCode(self,statusCode):

        self.statusCode = statusCode

    def addError(self,errormsg):

        self.errors.append(errormsg)

    def getFirstError(self):
        if len(self.errors) == 0:
            return None
        else:
            return self.errors[0]

    def getErrors(self):

        return self.errors

    # 是否有错误
    # <B> 说明： </B>
    # <pre>
    # 略
    # </pre>
    def hasError(self):

        # 校验是否有网络错误
        if self.hasNetworkError() == True:
            return True

        self.getData()

        if self.errors.count() > 0:
            return True
        else:
            return False

    def hasNetworkError(self):

        if self.networkError is not None:
            return self.networkError

        statusCode = str(self.getStatusCode())

        if not statusCode:
            self.addError('无法获取状态代码')
            return True

        if statusCode[0:2] == '20':
            #请求正常
            return False
        else:
            self.addError('头HTTP代码不等于20X，HTTP代码为{0}'.format(statusCode))
            return True;



