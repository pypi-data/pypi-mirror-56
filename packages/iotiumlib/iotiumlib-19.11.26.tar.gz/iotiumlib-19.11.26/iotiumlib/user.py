"""
// ========================================================================
// Copyright (c) 2018-2019 Iotium, Inc.
// ------------------------------------------------------------------------
// All rights reserved.
//
// ========================================================================
"""

__author__ = "Rashtrapathy"
__copyright__ = "Copyright (c) 2018-2019 by Iotium, Inc."
__license__ = "All rights reserved."
__email__ = "rashtrapathy.c@iotium.io"

from iotiumlib.requires.commonWrapper import *
from iotiumlib.requires.resourcePayload import *

userId = str()

class user(object):
    def __init__(self, action, payload=None, filters=None, user_id=None):

        if payload is None:
            payload = {}

        def getv2_user(uri):
            return user.User(self, method='getv2', uri=uri, filters=filters)

        def add_user(uri):
            return user.User(self, method='post', uri=uri)

        def edit_user(uri):
            return user.User(self, method='put', uri=uri)

        def delete_user(uri):
            return user.User(self, method='delete', uri=uri)

        _function_mapping = {
            'getv2': getv2_user,
            'add' : add_user,
            'edit' : edit_user,
            'delete':delete_user,
        }

        self.uri = {
            getv2_user: 'api/v2/user',
            add_user: 'api/v1/user',
            edit_user: 'api/v1/user/{userId}',
            delete_user: 'api/v1/user/{userId}',
        }

        self.payload = resourcePaylod.User(payload).__dict__

        self.userId = user_id

        self.Response = Response()

        _wrapper_fun = _function_mapping[action]
        args = '{}_user'.format(action)
        _wrapper_fun(self.uri[eval(args)])

    def User(self, method, uri, filters=None):

        respOp = dict()
        paramRequired = checkforUriParam(uri)
        if paramRequired:
            for param in paramRequired:
                uri = re.sub(r'{{{}}}'.format(param), eval('self.{}'.format(param)), uri)

        if method == 'get':
            respOp = getApi(formUri(uri))
        elif method == 'getv2':
            self.Response = getApiv2(formUri(uri), filters)
            return self.Response
        elif method == 'post':
            respOp = postApi(formUri(uri), self.payload)
        elif method == 'put':
            respOp = putApi(formUri(uri), self.payload)
        elif method == 'delete':
            respOp = deleteApi(formUri(uri))
        else:
            return self.Response
        self.Response.output = respOp.json()
        self.Response.code = respOp.status_code
        return self.Response

    @staticmethod
    def add(name, email, password, role, timezone=None):
        return user(action='add', payload=locals())

    @staticmethod
    def edit(user_id, name=None, role=None):
        return user(action='edit', payload=locals(), user_id=user_id)

    @staticmethod
    def delete(user_id):
        return user(action='delete', user_id=user_id)

    @staticmethod
    def getv2(filters=None):
        return user(action='getv2', filters=filters)

    def __del__(self):
        self.payload = dict()
        self.Response = Response()