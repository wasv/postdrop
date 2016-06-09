import base64
import os
import onetimepass as otp
from util import md5
from sqlalchemy import Column, Integer, String, Boolean, Text, Table, ForeignKey

from sqlalchemy.orm import relationship, backref

from postdrop.database import Base

tag_map = Table('tag_map',
                Base.metadata,
                Column('tag_id', Integer, ForeignKey('tags.id')),
                Column('note_id', Integer, ForeignKey('notes.id'))
                )

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(16), unique=True)
    otp_secret = Column(String(16))
    primary_key = Column(String(16))

    def generate_primary_key(self):
        self.primary_key = base64.b32encode(os.urandom(10)).decode('utf-8')

    def generate_otp_secret(self):
        self.otp_secret  = base64.b32encode(os.urandom(10)).decode('utf-8')

    def verify_auth_key(self, auth_key):
        return auth_key == md5(self.primary_key + str(otp.get_totp(secret=self.otp_secret)))

    def __repr__(self):
        return '<User %r>' % (self.username)

class Notes(Base):
    __tablename__ = 'notes'
    id = Column(Integer, primary_key=True)
    text = Column(Text(), unique=True)
    private = Column(Boolean)
    tags = relationship('Tag', secondary=tag_map,
                        backref=backref('photos', lazy='dynamic'))

class Tag(Base):
    __tablename__ = 'tags'
    id = Column(Integer, primary_key=True)
    name = Column(String(32), unique=True)