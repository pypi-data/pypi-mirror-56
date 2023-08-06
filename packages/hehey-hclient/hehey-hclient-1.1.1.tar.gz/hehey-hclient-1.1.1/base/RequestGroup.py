# -*- coding: utf-8 -*-

class RequestGroup(object):

    '''
        :type client: hclient.client.Client
    '''

    def __init__(self,client):

        self.index  = 0;
        self.requests = {}
        self.client = client;

    def service(self,siteName,url,data = {},index = '',**siteOptions):
        """
        :rtype:hclient.base.Request.Request
        :return:
        """
        request = self.client.service(siteName,url,data,**siteOptions);
        self._appendRequest(request,index);

        return self


    def get(self,url, data = {},index = '',**options):
        """
        :rtype:hclient.base.Request.Request
        :return:
        """
        request = self.client.get(url,data,**options)
        self._appendRequest(request, index);

        return self

    def post(self,url, data = {},index = '',**options):
        """
        :rtype:hclient.base.Request.Request
        :return:
        """

        request = self.client.post(url, data, **options)
        self._appendRequest(request, index);

        return self

    def put(self,url, data = {},index = '',**options):
        """
        :rtype:hclient.base.Request.Request
        :return:
        """

        request = self.client.put(url, data, **options)
        self._appendRequest(request, index);

        return self

    def patch(self,url, data = {},index = '',**options):
        """
        :rtype:hclient.base.Request.Request
        :return:
        """
        request = self.client.patch(url, data, **options)
        self._appendRequest(request, index);

        return self

    def delete(self,url, data = {},index = '',**options):
        """
        :rtype:hclient.base.Request.Request
        :return:
        """
        request = self.client.delete(url, data, **options)
        self._appendRequest(request, index);

        return self

    def head(self,url, data = {},index = '',**options):
        """
        :rtype:hclient.base.Request.Request
        :return:
        """
        request = self.client.head(url, data, **options)
        self._appendRequest(request, index);

        return self

    def options(self,url, data = {},index = '',**options):
        """
        :rtype:hclient.base.Request.Request
        :return:
        """
        request = self.client.options(url, data, **options)
        self._appendRequest(request, index);

        return self


    def send(self):


        return self.client.batchSend(self.requests)

    def _appendRequest(self,request,index):

        requestIndex = '';
        if not index:
            requestIndex = self.index;
        else:
            requestIndex = index;

        self.index = self.index + 1;
        self.requests[str(requestIndex)] = request;

        return ;

