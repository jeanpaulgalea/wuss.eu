from datetime import datetime
from random import choice
from string import letters, digits
from uuid import uuid4

from redis import StrictRedis

from .exceptions import NotFound, AuthFailure


class Link(object):

    def __init__(self):
        self.r = StrictRedis(host='192.168.56.120', port=6379, db=0)

    def shorten(self, link):
        """
        """
        while True:
            hash = self._hash()
            if self.r.hsetnx(hash, 'link', link):
                break

        uuid = self._uuid()
        date = self._date()

        self.r.hset(hash, 'uuid', uuid)
        self.r.hset(hash, 'hits', 0)
        self.r.hset(hash, 'mods', 0)
        self.r.hset(hash, 'created_at', date)
        self.r.hset(hash, 'lasthit_at', None)
        self.r.hset(hash, 'changed_at', None)

        return hash, uuid

    def modify(self, hash, uuid, link):
        """
        """
        if not (self.r.hget(hash, 'uuid') == uuid.lower()):
            raise AuthFailure

        self.r.hset(hash, 'link', link)
        self.r.hincrby(hash, 'mods', 1)
        self.r.hset(hash, 'changed_at', self._date())

    def resolve(self, hash):
        """
        """
        link = self.r.hget(hash, 'link')

        if link is None:
            raise NotFound

        self.r.hincrby(hash, 'hits', 1)
        self.r.hset(hash, 'lasthit_at', self._date())

        return link

    def exists(self, hash):
        """
        """
        return self.r.exists(hash)

    def _hash(self, length=7):
        return ''.join(choice(letters + digits) for _ in range(length))

    def _uuid(self):
        return str(uuid4())

    def _date(self):
        return str(datetime.utcnow().replace(microsecond=0))
