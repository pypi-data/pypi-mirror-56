class Measurement(object):
    def __init__(self, document: object):
        self.document = document
        pass

    def getType(self) -> str:
        return self.document.get('type')

    def getId(self) -> str:
        return self.document.get('id')

    def getDocument(self) -> object:
        return self.document.get('fields')