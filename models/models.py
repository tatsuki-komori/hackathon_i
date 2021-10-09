from sqlalchemy import Column, Integer, String, Boolean, Text, DateTime
from sqlalchemy.orm import backref, relation, relationship
from sqlalchemy.sql.schema import ForeignKey
from models.database import Base
from datetime import datetime

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, nullable=False)
    user_name = Column(String(128), unique=True, nullable=False)
    hashed_password = Column(String(128), nullable=False)
    menter_id = Column(Integer, nullable=False)
    team_name = Column(String(128))

    def __init__(self, user_name, hashed_password, menter_id):
        self.user_name = user_name
        self.hashed_password = hashed_password
        self.menter_id = menter_id
        self.team_name = ''

    def __repr__(self):
        return '<Name %r>' % (self.user_name)

class Task(Base):
    __tablename__ = 'tasks'
    id = Column(Integer, primary_key=True, nullable=False)
    content = Column(Text, nullable=False)
    detail = Column(Text)
    completed = Column(Boolean, default=False)
    user_id = Column(Integer, ForeignKey('users.id'))

    user = relationship("User", backref=backref('tasks', order_by=id), cascade="delete")

    def __init__(self, content, detail, user_id):
        self.content = content
        self.detail = detail
        self.user_id = user_id
    
    def __repr__(self):
        return '<Task %r>' % self.content
