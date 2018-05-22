from abc import ABCMeta, abstractmethod


class BaseRepository:
    __metaclass__ = ABCMeta

    # get one model
    @abstractmethod
    def get(self, **pk):
        pass

    @abstractmethod
    def get_or_404(self, **keys):
        pass

    # find all models filtered by some conditions
    @abstractmethod
    def find(self, **keys):
        pass

    @abstractmethod
    def add(self, entity):
        pass

    @abstractmethod
    def add_all(self, entities):
        pass

    @abstractmethod
    def delete(self, entity):
        pass

    @abstractmethod
    def create(self, **kw):
        pass

    @abstractmethod
    def all(self):
        pass
