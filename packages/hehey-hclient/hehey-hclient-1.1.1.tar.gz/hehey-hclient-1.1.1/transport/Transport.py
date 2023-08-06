
import abc
from ..utils.ClientUtil import ClientUtil
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
class Transport(object):

    @classmethod
    def make(cls, transportName) -> 'Transport':
        if not transportName:
            raise RuntimeError('transport {0} is empty'.format(transportName))

        if transportName.find('.') == -1:
            transportClazzName = ClientUtil.ucfirst(transportName) + 'Transport'
            transportClazz = __package__ + "." + transportClazzName + '.' + transportClazzName
        else:
            transportClazz = transportName

        transportMeta = ClientUtil.getModuleMeta(transportClazz)

        return transportMeta()


    @abc.abstractmethod
    def send(self,request):
        pass

    def batchSend(self,requests)->'dict':

        for key, request in requests.items():
            self.send(request)

