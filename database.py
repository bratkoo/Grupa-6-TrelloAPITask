from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


class DatabaseConnection:
    def __init__(self, db_url):
        self.engine = create_engine(db_url)
        self.Session = sessionmaker(bind=self.engine)

    def get_session(self):
        return self.Session()

    def create(self, obj):
        session = self.get_session()
        session.add(obj)
        session.commit()
        session.close()

    def read(self, model, filters=None):
        session = self.get_session()
        query = session.query(model)
        if filters:
            query = query.filter_by(**filters)
        result = query.all()
        session.close()
        return result

    def update(self, obj):
        session = self.get_session()
        session.merge(obj)
        session.commit()
        session.close()

    def delete(self, obj):
        session = self.get_session()
        session.delete(obj)
        session.commit()
        session.close()

