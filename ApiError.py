# -*- coding: utf-8 -*-
'''
Created on 2012-3-27

@author: zhangdong
'''

class APIError(StandardError):
    '''
    raise APIError if got failed json message.
    '''
    def __init__(self, error_code, error, uri):
        self.error_code = error_code
        self.error = error
        self.uri = uri
        StandardError.__init__(self, error)

    def __str__(self):
        return 'APIError: %s: %s, uri: %s' % (self.error_code, self.error, self.uri)
