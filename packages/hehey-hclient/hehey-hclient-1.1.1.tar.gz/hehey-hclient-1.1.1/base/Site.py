# -*- coding: utf-8 -*-
from .Request import Request
from ..utils.ClientUtil import ClientUtil

"""
 * 服务站点
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
class Site(object):

    '''
        :type client: hclient.client.Client
    '''

    def __init__(self,options = {},client = None):

        self.client = client;
        self.options = options;

        return ;


    def setClient(self,client):

        self.client = client

        return self;

    # 创建请求对象
    # <B> 说明： </B>
    # <pre>
    # 略
    # </pre>
    def createRequest(self,options = {})->'Request':

        requestOptions = options.copy()
        requestClazz = requestOptions.get('clazz', None)
        transport = requestOptions.get('transport', None)

        if transport is None:
            requestOptions['transport'] = self.transport

        if requestClazz is None:
            requestClazz = Request;
        else:
            if requestClazz.find('.') == -1:
                requestClazz = ClientUtil.buildClazzModule(ClientUtil.dirname(__package__) + ".protocol",
                                                           requestClazz, 'Request');

        requestMeta = ClientUtil.getModuleMeta(requestClazz)
        request = requestMeta(requestOptions)
        request.setClient(self.client)

        return request

    # 发送服务请求
    # <B> 说明： </B>
    # <pre>
    # 略
    # </pre>
    def service(self,url,data = {},**siteOptions)->'Request':

        siteConf = self.options.copy();

        requestConf = {}
        requestConf.update(siteConf)
        requestConf.update(siteOptions)
        request = self.createRequest(requestConf)
        request.setUrl(url)

        if isinstance(data, dict):
            request.setData(data)
        else:
            request.setContent(data)

        return request

    # 发送服务请求
    # <B> 说明： </B>
    # <pre>
    # 略
    # </pre>
    def serviceResult(self, url, data={}, **siteOptions):

        request = self.service(url,data,**siteOptions)

        return request.send().getData()



