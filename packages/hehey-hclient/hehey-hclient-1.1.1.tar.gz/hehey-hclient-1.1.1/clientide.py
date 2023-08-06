from hclient.client import Client

class IdeClient(Client):

    def serviceResult(self, siteName, url, data={}, **siteOptions):
        pass;

    def getResult(self, url, data={}, **options):
        pass;

    def postResult(self, url, data={}, **options):
        pass;

    def putResult(self, url, data={}, **options):
        pass;

    def patchResult(self, url, data={}, **options):
        pass;

    def deleteResult(self, url, data={}, **options):
        pass;

    def headResult(self, url, data={}, **options):
        pass;

    def optionsResult(self, url, data={}, **options):
        pass;

