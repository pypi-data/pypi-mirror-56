
from ..base.Request import Request
from urllib.parse import urlparse

class HttpRequest(Request):


    def prepare(self):

        super().prepare()
        pathInfo = urlparse(self.getFullUrl())

        if pathInfo.netloc.find(':') != -1:
            netloc = pathInfo.netloc.rsplit(':', 1)
            self.host = netloc[0];
            self.port = netloc[1];
        else:
            self.host = pathInfo.netloc

        if pathInfo.scheme in ['http','https']:
            self.scheme = 'tcp'
        else:
            self.scheme = pathInfo.scheme


    def buildRequestContent(self):
        requestHeaders = self.formatHeaders()
        requestData =  self.getContent();
        method = self.getMethod().upper()
        pathInfo = urlparse(self.getFullUrl())
        requestHeaders.insert(0,'{0} {1} HTTP/1.0'.format(method,pathInfo.path));
        requestHeaders.append('Host: {0}'.format(pathInfo.netloc));
        requestHeaders.append('Content-Length: {0}'.format(len(requestData)));
        requestHeaders.append('Content-Connection: close');
        requestHeaders.append('Accept: */*');

        return '\r\n'.join(requestHeaders) + '\r\n\r\n' + requestData
