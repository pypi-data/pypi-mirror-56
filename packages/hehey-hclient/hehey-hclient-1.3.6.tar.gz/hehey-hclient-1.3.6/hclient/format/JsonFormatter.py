
from .Formatter import Formatter
import json

class JsonFormatter(Formatter):


    def format(self,request):
        """
        :type request : hclient.base.Request.Request
        """
        request.setContent(json.dumps(request.getContent()));
        request.addHeaders('Content-Type', 'application/json; charset=UTF-8')

        return ;
