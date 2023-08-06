
from ..base.Response import Response

class ServiceResponse(Response):

    def __init__(self,attrs = {}):

        self.varCode = 'code'

        self.varMsg = 'message'

        self.varResult = 'data'

        self.defaultCode = 0

        self.errcode = ''

        self.errmsg = ''

        self._init = False

        if attrs:
            super().__init__(attrs)

    # 检查业务是否错误
    # <B> 说明： </B>
    # <pre>
    # 略
    # </pre>
    def check(self,errorCode = []):

        self.__initData()

        if not errorCode:
            errorCode = [self.defaultCode]

        if self.errcode in errorCode:
            return True
        else:
            return False


    def getCode(self):

        self.__initData()

        return self.errcode

    def getMessage(self):

        self.__initData()

        return self.errmsg

    def getResult(self):

        data = self.getData()
        result = data.get(self.varResult,None)

        return result

    def __initData(self):

        if self._init:
            return

        data = self.getData()

        self.errmsg = data.get(self.varMsg,None)
        self.errcode = data.get(self.varCode, None)
        self._init = True



