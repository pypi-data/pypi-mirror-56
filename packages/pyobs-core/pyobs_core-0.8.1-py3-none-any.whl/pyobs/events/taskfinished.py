from .event import Event


class TaskFinishedEvent(Event):
    def __init__(self, name: str = None):
        Event.__init__(self)
        self.data = {'name': name}

    @property
    def name(self):
        return self.data['name']


__all__ = ['TaskFinishedEvent']
