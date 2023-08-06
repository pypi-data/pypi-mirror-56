from meapy import MeaPy


class MeasurementList:
    def __init__(self, meapy: MeaPy):
        self.meapy = meapy

    def items(self, query: str):
        index = 0
        currentItems = self.meapy.search(query)
        while currentItems and index < len(currentItems):
            yield currentItems[index]
            index += 1
            if(index == 100):
                currentItems = self.meapy.search(query)
                index = 0
