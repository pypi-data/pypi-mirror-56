
from .Transport import Transport
import socket

"""
 * socket 传输协议基类
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
class SocketTransport(Transport):

    READ_BUFFER_SIZE = 65535

    def send(self,request):

        clientSocket = self.initSocket(request)
        responseRawContent = self.readSocket(clientSocket);
        clientSocket.close()
        response = request.createResponse(responseRawContent)

        return request

    def initSocket(self,request):

        request.prepare()
        socketAddr = (request.getHost(), request.getPort())

        if request.getScheme() == 'tcp':
            clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        else:
            clientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        clientSocket.connect(socketAddr)
        requestRawContent = request.buildRequestContent()
        clientSocket.send(requestRawContent.encode())

        return clientSocket;


    def readSocket(self,clientSocket:socket):

        recvBuffer = []
        while (True):
            buffer = clientSocket.recv(self.READ_BUFFER_SIZE)
            if len(buffer) <= 0:
                break
            recvBuffer.append(buffer.decode('utf-8'))

        body = ''.join(recvBuffer)

        return body;


    def batchSend(self, requests):

        clientSockets = {};

        for (index, request) in requests.items():
            clientSocket = self.initSocket(request)
            clientSockets[index] = clientSocket

        for (index, clientSocket) in clientSockets.items():
            request = requests.get(index)
            try:
                clientSocket = self.initSocket(request)
                responseRawContent = self.readSocket(clientSocket);
                clientSocket.close()
                response = request.createResponse(responseRawContent)
            except Exception as e:
                response = request.createResponse('')
                response.addError(str(e))

        pass





