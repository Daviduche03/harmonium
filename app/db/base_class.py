from sqlalchemy.ext.declarative import declarative_base, declared_attr
from sqlalchemy.orm import as_declarative, declared_attr

@as_declarative()
class Base:
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    id: any
    __name__: str