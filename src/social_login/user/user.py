# -*- coding: utf-8 -*-

import sys

sys.path.append("..")


class User():
    def __init__(self, dic):
        for key, value in dic.iteritems():
            setattr(self, key, value)

    def get_user_id(self):
        return self.id

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return unicode(self.get_user_id())

    def is_super(self):
        return self.is_super

    def __repr__(self):
        return repr(self.__dict__)
