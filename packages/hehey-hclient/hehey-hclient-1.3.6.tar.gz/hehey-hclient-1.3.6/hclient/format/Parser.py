
import abc
from ..utils.ClientUtil import ClientUtil

class Parser(object):

    @classmethod
    def make(self, parserName):

        if not parserName:
            raise RuntimeError('Parser is empty')

        if parserName.find('.') == -1:
            clazzName = ClientUtil.ucfirst(parserName) + 'Parser'
            parserClazz = __package__ + "." + clazzName + '.' + clazzName
        else:
            parserClazz = parserName

        parserMeta = ClientUtil.getModuleMeta(parserClazz)

        return parserMeta()

    @abc.abstractmethod
    def format(self, response):

        pass
