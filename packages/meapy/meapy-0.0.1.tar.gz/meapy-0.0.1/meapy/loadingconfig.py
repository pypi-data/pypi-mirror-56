class LoadingConfig(object):
    def __init__(self):
        pass

    def withTemplate(self, uid: str):
        self.templateUid = uid
        return self

    def withSignals(self, signals: list):
        self.signals = signals
        return self
