from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from db.session import db_engine

ModelBase = declarative_base(bind=db_engine)


class User(ModelBase):

    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String)
    password = Column(String)
    role_id = Column(Integer, ForeignKey('user_role.id'))

    def __init__(self, name, email, passwd):
        self.name = name
        self.email = email
        self.password = passwd
        self.role_id = 0

    def __repr__(self):
        return "id: {}\tname: {}".format(self.id, self.name)


class UserRole(ModelBase):

    __tablename__: str = 'user_role'

    id = Column(Integer, primary_key=True)
    roleName = Column(String)
    users = relationship('User', backref='users', lazy='dynamic')

    def __init__(self, name):
        self.roleName = name

    def __repr__(self):
        return "id {}\troleName {}".format(self.id, self.roleName)
