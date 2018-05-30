from abc import ABCMeta, abstractmethod

from  werkzeug.exceptions import Aborter
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


class SQLAlchemyRepository(BaseRepository):

    def __init__(self, model, session):
        self.model = model
        self.session = session




    def get(self, **pk):
        return self.session.query(self.model).filter_by(**pk).one()

    def get_or_404(self, **keys):
        rv = self.session.query(self.model).filter_by(**keys).one()
        if rv is None:
            Aborter.abort(404)
        return rv

    # find all models filtered by some conditions
    def find(self, **keys):
        self.session.query(self.model).filter_by(**keys).first()


    def add(self, entity):
        self.session.add(entity)
        self.session.commit()


    def add_all(self, entities):
        self.session.add(entities)
        self.session.commit()


    def delete(self, entity):
        self.session.delete(entity)
        self.session.commit()

    def create(self, **kw):
        return self.model(**kw)


    def all(self):
        return list(self.session.query(self.model).all())


