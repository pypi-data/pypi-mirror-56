# -*- coding: utf-8 -*-
from ..utils.ClientUtil import ClientUtil
from .Request import Request
from .Site import Site
from .Response import Response
from ..transport.Transport import Transport
from ..format.Formatter import Formatter
from ..format.Parser import Parser
from ..protocol.ServiceResponse import ServiceResponse
from .RequestGroup import RequestGroup

"""
 * client 客户端
 *<B>说明：</B>
 *<pre>
 * 关键词:request,response,transport(传输协议),format(序列化),Parse(反序列化),Api(外部系统api)
 * 一个url 就是一个Request 类
 * client 单例类
 *</pre>
 *<B>示例：</B>
 *<pre>
 * 实例1:GET HTTP 请求,支持OPTIONS, GET, HEAD, POST, PUT, DELETE, TRACE, CONNECT
 * client = Client()
 * response = client.post('http://www.baidu.com/',{'user_id':2}).send()
 * 获取返回结果
 * response.getData()
 *
 * 实例2:设置request,respone 数据为json格式,json 可为类命名空间
 * response = client.post('http://www.baidu.com/',{'user_id':2}).setFormat('json').send();
 * response.setFormat('json').getData()
 * 实例3:批量请求GET,POST
 * request1 = client.post('http://www.baidu.com/',{'user_id':2}).setFormat('json')
 * request2 = client.post('http://www.baidu.com/',{'user_id':2}).setFormat('json')
 * requests = {
 *   'user1':request1,
 *   'user2':request2
 * }
 * responses = client.batchSend(requests);
 * responses['user1'].setFormat('json').getData();
 * 
 * 实例4:验证http 错误
 * response = client.post('http://www.baidu.com/',{'user_id':2}).send();
 * 验证是否错误,验证网络,解析数据,Transport（传输层） 是否有错误
 * response.hasError()
 *
 * 验证是否网络错误,主要验证header http-code 状态码 是否等于20x
 * response.hasNetworkError()
 *
 * 获取错误信息
 * response.getErrors()
 * response.getFirstError()
 * 
 * api 接口示例
 * response = client.service('mba','system/site/getConfInfo',{"id":1}).send()
 * 
 * 基本配置
 * {
     'mba':{
            'clazz':'request class name',# request 类名,比如http
            'host':'http://eduapi.yesmba.cn/',# 接口host 地址
            'format':'json',# 数据格式类型,
            'headers':{},# 默认header 信息
            'options':{},# 传输协议配置
            'method':'POST',
            'response':{
                'clazz':'service',
                'format':"json"
            }
        },
   }
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
class BaseClient(object):

    def __init__(self,**attrs):

        # 服务站点对象
        # <B> 说明： </B>
        # <pre>
        # 略
        # </pre>
        self.sites = {}

        # 客户自定义站点配置
        # <B> 说明： </B>
        # <pre>
        # 略
        # </pre>
        self.customSites = {};

        # 默认传输协议
        # <B> 说明： </B>
        # <pre>
        # 略
        # </pre>
        self.transport = 'Curl'

        # 协议对象列表
        # <B> 说明： </B>
        # <pre>
        # 略
        # </pre>
        self._transportCache = {}

        # 格式化对象列表
        # <B> 说明： </B>
        # <pre>
        # 略
        # </pre>
        self._formatterCache = {}

        # 解析对象列表
        # <B> 说明： </B>
        # <pre>
        # 略
        # </pre>
        self._parserCache = {}


        if attrs:
            ClientUtil.setAttrs(self,attrs)

        # 生成代理方法
        self.createResultMethod();

    def setTransport(self,transport):

        self.transport = transport

    # 创建一个传输协议对象
    # <B> 说明： </B>
    # <pre>
    # 单例
    # </pre>
    def getTransport(self,transportName = '')->'Transport':

        if not transportName:
            transportName = self.transport

        transportObj = self._transportCache.get(transportName,None)
        if transportObj is None:
            transportObj = Transport.make(transportName);
            self._transportCache[transportName] = transportObj


        return transportObj

    # 获取格式化对象
    # <B> 说明： </B>
    # <pre>
    # 单例
    # </pre>
    def getFormatter(self,formatName):

        formatObj = self._formatterCache.get(formatName, None)

        if formatObj is None:
            formatObj = Formatter.make(formatName)
            self._formatterCache[formatName] = formatObj

        return formatObj

    # 获取格式化对象
    # <B> 说明： </B>
    # <pre>
    # 单例
    # </pre>
    def getParser(self, parserName):

        parserObj = self._parserCache.get(parserName, None)

        if parserObj is None:
            parserObj = Parser.make(parserName)
            self._parserCache[parserName] = parserObj

        return parserObj

    # 获取服务站点对象
    # <B> 说明： </B>
    # <pre>
    # 单例
    # </pre>
    def getSite(self,siteName)->'Site':

        site = self.sites.get(siteName,None)
        if site:
            return site;

        # 创建对象
        siteConf = self.customSites.get(siteName,None)
        if siteConf is None:
            raise Exception("site {0} no find".format(siteName))

        site = Site(siteConf)
        site.setClient(self);

        self.sites[siteName] = site

        return site;


    # 创建request 对象
    # <B> 说明： </B>
    # <pre>
    # 单例
    # </pre>
    def createRequest(self,options = {})->'Request':

        requestOptions = options.copy()
        requestClazz = requestOptions.get('clazz',None)
        transport = requestOptions.get('transport',None)

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
        request.setClient(self)

        return request


    def createResponse(self,options)->'Response':

        responseClazz = options.get('clazz', None)

        if responseClazz is None:
            responseClazz = Response;
        else:
            if responseClazz.find('.') == -1:
                responseClazz = ClientUtil.buildClazzModule(ClientUtil.dirname(__package__) + ".protocol",responseClazz,'Response');


        responseMeta = ClientUtil.getModuleMeta(responseClazz)

        response = responseMeta(options)
        response.setClient(self)

        return response

    # request 发送请求
    # <B> 说明： </B>
    # <pre>
    # 单例
    # </pre>
    def send(self,request:Request)->'ServiceResponse':

        self.getTransport(request.getTransport()).send(request)

        return request.getResponse()

    # 批量发送请求
    # <B> 说明： </B>
    # <pre>
    # 单例
    # </pre>
    def batchSend(self, requests = []):

        requestList = {}
        if isinstance(requests,list):
            for i in range(len(requests)):
                requestList[str(i)] = requests[i]
            requests = requestList;


        transportRequestList = self.classRequestsByTransport(requests);

        for transport,requestList in transportRequestList.items():
            self.getTransport(transport).batchSend(requestList)

        responses = {}
        for index,request in requests.items():
            responses[index] = request.getResponse()

        return responses;

    # 批量请求
    # <B> 说明： </B>
    # <pre>
    # 单例
    # </pre>
    def batch(self)->'RequestGroup':

        return RequestGroup(self)

    # 按传输协议归类请求
    # <B> 说明： </B>
    # <pre>
    # 单例
    # </pre>
    def classRequestsByTransport(self,requests = {})->dict:

        newRequests = {}
        for index,request in requests.items():
            transport = request.getTransport()
            requestList = newRequests.get(transport,None)
            if requestList is None:
                requestList = {}
            requestList[index] = request

            newRequests[transport] = requestList

        return newRequests;


    # 通过快捷方式创建一个request 请求
    # <B> 说明： </B>
    # <pre>
    # 单例
    # </pre>
    def createRequestShortcut(self,method, url, data,**requestConf)->'Request':

        request = self.createRequest(requestConf)
        request.setClient(self).setMethod(method).setUrl(url).setData(data)

        if isinstance(data, dict):
            request.setData(data)
        else:
            request.setContent(data)

        return request


    # http 快捷方式： OPTIONS, GET, HEAD, POST, PUT, DELETE, TRACE, CONNECT
    def service(self,siteName,url,data = {},**siteOptions)->'Request':

        site = self.getSite(siteName)
        request = site.service(url,data,**siteOptions);

        return request

    def get(self,url, data = {},**options)->'Request':

        return self.createRequestShortcut('GET',url,data,**options)

    def post(self,url, data = {},**options)->'Request':

        return self.createRequestShortcut('POST',url,data,**options)

    def put(self,url, data = {},**options)->'Request':

        return self.createRequestShortcut('PUT',url,data,**options)

    def patch(self,url, data = {},**options)->'Request':

        return self.createRequestShortcut('PATCH',url,data,options)

    def delete(self,url, data = {},**options)->'Request':

        return self.createRequestShortcut('DELETE',url,data,**options)

    def head(self,url, data = {},**options)->'Request':

        return self.createRequestShortcut('HEAD',url,data,**options)

    def options(self,url, data = {},**options)->'Request':

        return self.createRequestShortcut('OPTIONS',url,data,**options)

    def createResultMethod(self):

        methods = ['service','get','post','put','patch','delete','head','options'];
        for method in methods:
            methodTemplate = """
def {0}(self,*args,**kwargs):
    reqeust = self.{1}(*args,**kwargs)
    return reqeust.send().getData();
                     """
            agentMethod = method + 'Result';
            methodCodeStr = methodTemplate.format(agentMethod,method)
            ClientUtil.buildAgentMethod(self,methodCodeStr,agentMethod)

        return ;

    def __getattr__(self, siteName):

        """
        :rtype:Site
        :return:
        """
        return self.getSite(siteName)
