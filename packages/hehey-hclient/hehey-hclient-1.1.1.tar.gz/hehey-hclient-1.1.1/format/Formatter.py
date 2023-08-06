
import abc
from ..utils.ClientUtil import ClientUtil

class Formatter(object):

    @classmethod
    def make(self, formatName):

        if not formatName:
            raise RuntimeError('format is empty')

        if formatName.find('.') == -1:
            clazzName = ClientUtil.ucfirst(formatName) + 'Formatter'
            formatClazz = __package__ + "." + clazzName + '.' + clazzName
        else:
            formatClazz = formatName

        formatMeta = ClientUtil.getModuleMeta(formatClazz)

        return formatMeta()

    @abc.abstractmethod
    def format(self,request):

        pass
