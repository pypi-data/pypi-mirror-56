
from .Parser import Parser
import json

class JsonParser(Parser):

    def format(self,response):

        response.setData(json.loads(response.getContent()));

        return ;
