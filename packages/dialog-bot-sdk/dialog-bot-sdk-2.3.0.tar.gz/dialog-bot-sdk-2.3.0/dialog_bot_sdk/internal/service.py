class AuthenticatedService(object):
    """Initialization class for gRPC services.

    """
    def __init__(self, auth_token_func, stub, verbose=False):
        self.stub = stub
        self.auth_token_func = auth_token_func
        self.verbose = verbose
        for method_name in dir(stub):
            method = getattr(stub, method_name)
            if not method_name.startswith('__') and callable(method):
                setattr(self, method_name, self.__decorated(method_name, method))

    def __decorated(self, method_name, method):
        def inner(param):
            auth_token = self.auth_token_func()
            if self.verbose:
                print('Calling %s with token=`%s`' % (method_name, auth_token))
            if auth_token is not None:
                metadata = (('x-auth-ticket', auth_token),)
            else:
                metadata = None
            return method(param, metadata=metadata)
        return inner
